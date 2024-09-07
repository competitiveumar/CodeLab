from django.urls import re_path  # Import re_path for defining URL patterns
from CodeLabWebsite.consumers import ChatConsumer  # Import ChatConsumer from the consumers module

# Define WebSocket URL patterns
websocket_urlpatterns = [
    # Route WebSocket connections to ChatConsumer, capturing the room_name parameter
    re_path(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
]