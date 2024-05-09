import os

from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application
from django.core.asgi import get_asgi_application

django_asgi_app = get_asgi_application()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "creatorhero.settings")
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter , URLRouter
from chat import urls
application = ProtocolTypeRouter(
    {
        "http" : get_asgi_application() , 
        "websocket" : AuthMiddlewareStack(
            URLRouter(
                urls.urlpatterns
            )    
        )
    }
)
ASGI_APPLICATION = 'creatorhero.asgi.application'
