from django.utils import timezone

from .models import VSServer


def get_client_ip(request) -> str:
    """
    Extract ip address of request client, first checking for if a proxy is used
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def vs_prune_old_servers(age_mins: int = 10) -> int:
    """
    Check database for entries that haven't been updated for over `age` minutes and delete them, assuming them to
    have gone offline.

    :returns: int as a count of server listings removed from the database.
    """
    counter = 0
    for server in VSServer.objects.all():
        if server.last_heartbeat < timezone.now() - timezone.timedelta(minutes=age_mins):
            server.delete()
            counter += 1
    return counter
