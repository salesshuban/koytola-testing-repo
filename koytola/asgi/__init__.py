"""ASGI config for Koytola project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

# import os
#
# from django.core.asgi import get_asgi_application
#
# from koytola.asgi.health_check import health_check
#
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "koytola.settings")
#
# application = get_asgi_application()
# application = health_check(application, "/health/")
import django
django.setup()
import os
from channels.auth import AuthMiddlewareStack

from channels.routing import ProtocolTypeRouter, URLRouter
from ..product import routing, ChatAuthentication
from django.core.asgi import get_asgi_application
django_asgi_app = get_asgi_application()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'koytola.settings')

application = ProtocolTypeRouter({
  "http": django_asgi_app,
  "websocket": ChatAuthentication.CustomAuthentication(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
})

