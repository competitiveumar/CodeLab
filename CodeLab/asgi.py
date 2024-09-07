"""
ASGI config for CodeLab project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from CodeLabWebsite.routing import websocket_urlpatterns

# Set the default settings module for the 'django' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CodeLab.settings')

# Define the ASGI application.
application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # HTTP protocol
    "websocket": AuthMiddlewareStack(  # WebSocket protocol with authentication
        URLRouter(
            websocket_urlpatterns  # WebSocket URL patterns
        )
    ),
})