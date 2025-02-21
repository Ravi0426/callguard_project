import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import features.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'callguard_project.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            features.routing.websocket_urlpatterns
        )
    ),
})
