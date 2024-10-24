from django.urls import re_path
from .consumers import MandrillEventConsumer

websocket_urlpatterns = [
    re_path(r'ws/notifications/$', MandrillEventConsumer.as_asgi()),  # WebSocket route
]
