from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/monitor/<room_name>', consumers.MonitorConsumer, name='room'),
]