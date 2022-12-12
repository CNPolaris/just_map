from django.urls import re_path
from channels.routing import ProtocolTypeRouter, URLRouter

from ws import consumers

websocket_urlpatterns = [
    re_path(r'ship/data/(?P<group>\w+)/$', consumers.DataConsumer.as_asgi()),
    re_path(r'ship/video/(?P<group>\w+)/$', consumers.VideoDataConsumer.as_asgi())
]