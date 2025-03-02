from django.urls import path

from . import views

app_name = "vsmaster"

urlpatterns = [
    path('register', views.VSMasterRegister.as_view(), name='vsregister'),
    path('heartbeat', views.VSMasterHeartbeat.as_view(), name="vsheartbeat"),
    path('unregister', views.VSMasterUnregister.as_view(), name="vsunregister"),
    path('list', views.VSMasterList.as_view(), name="vslist"),
]
