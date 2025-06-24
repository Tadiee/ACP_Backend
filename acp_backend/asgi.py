"""
ASGI config for acp_backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from system_files.routing import websocket_urlpatterns  # <-- import from step 1

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'acp_backend.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    
    # "websocket": AuthMiddlewareStack(
    #     URLRouter(websocket_urlpatterns)
    # ),
    
})
