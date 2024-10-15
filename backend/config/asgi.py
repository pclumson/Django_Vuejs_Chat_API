"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""
#
# import os
#
# from django.core.asgi import get_asgi_application
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
#
# application = get_asgi_application()


import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from django.urls import path

from django.conf import settings

import chat.ws_urls
from config import settings
from config import asgi




os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()


from chat.consumers.message import MessageConsumer
from chat.consumers.notification import NewUserConsumer
#
# from chat.consumers import AdminChatConsumer, PublicChatConsumer

application = ProtocolTypeRouter({
    # Django's ASGI application to handle traditional HTTP requests
    "http": django_asgi_app,

    # WebSocket chat handler
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter([
                # path("chat/admin/", AdminChatConsumer.as_asgi()),
                # path("chat/", PublicChatConsumer.as_asgi()),
                path('ws/notification/', NewUserConsumer.as_asgi()),
                path('ws/message/<str:username>/', MessageConsumer.as_asgi())

            ])
        )
    ),
})









#
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
#
# application = ProtocolTypeRouter({
#
#     "http": get_asgi_application(),
#
#     "websocket": AuthMiddlewareStack(
#
#         URLRouter(chat.ws_urls.websocket_urlpatterns)
#     )
# })
