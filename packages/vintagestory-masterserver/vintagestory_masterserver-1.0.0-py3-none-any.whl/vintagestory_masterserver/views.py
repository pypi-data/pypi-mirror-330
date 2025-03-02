import json
from django.http import JsonResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View

import socket

from .utils import get_client_ip, vs_prune_old_servers
from .models import VSServer


class CSRFExemptMixin:
   @method_decorator(csrf_exempt)
   def dispatch(self, *args, **kwargs):
       return super(CSRFExemptMixin, self).dispatch(*args, **kwargs)


class VSMasterRegister(CSRFExemptMixin, View):
    def post(self, request):
        data = json.loads(request.body)
        ip = get_client_ip(request)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # Check if port is open -- probably a better way to do this?
            result = sock.connect_ex((ip, data['port']))
            if result == 0:
                server = VSServer.objects.create_server(data, ip)
                # vs_check_server_still_alive(server.token)
                resp = {"data": server.token, "status": "ok"}
            else:
                resp = {"status":"bad", "data":"port not opened"}

        return JsonResponse(resp)


class VSMasterHeartbeat(CSRFExemptMixin, View):
    def post(self, request):
        data = json.loads(request.body)
        server: VSServer = VSServer.objects.filter(token=data['token']).first()
        if server:
            server.last_heartbeat = timezone.now()
            server.players = data['players']
            server.save()
            return JsonResponse({"status": "ok"})
        else:
            return JsonResponse({"status": "timeout", "data": "timeout"})  # game server should re-register itself


class VSMasterUnregister(CSRFExemptMixin, View):
    def post(self, request):
        data = json.loads(request.body)
        server: VSServer = VSServer.objects.filter(token=data['token']).first()
        server.delete()
        return JsonResponse({"status": "ok"})


class VSMasterList(CSRFExemptMixin, View):
    def get(self, request):
        # got only servers that have provided a heartbeat recently.
        servers = VSServer.objects.filter(last_heartbeat__gte=timezone.now()-timezone.timedelta(minutes=6))
        server_list = [server.as_dict() for server in servers]
        return JsonResponse(
            {
                "status": "ok",
                "data": server_list
            }
        )

class VSMasterPruneDB(CSRFExemptMixin, View):
    """
    In theory servers should unregister themselves when they exit, and will be gracefully removed from the database.
    In reality someone is going to force kill a server and leave it hanging around. Ideally you will set up a background
    task using cron/celery/whatever that periodically wipes the database of aged entries by calling
    `utils.vs_prune_old_servers()`

    But if you don't care about the potential issues, this endpoint is provided (but not given a URL by default)
    to trigger such a pruning.
    """
    def get(self, request):
        vs_prune_old_servers(10)

