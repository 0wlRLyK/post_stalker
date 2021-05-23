"""
ASGI config for post_stalker project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.conf.urls import url

from chat.consumers import DialogConsumer, ChatConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'post_stalker.settings')

application = ProtocolTypeRouter({
    # Websocket chat handler
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                [
                    # url(r"chat/", DialogConsumer, name='chat')
                    url(r"d/(?P<username>[\w.@+-]+)/$", DialogConsumer.as_asgi(), name='dialog'),
                    url(r"chat/(?P<slug>[\w.@+-]+)/$", ChatConsumer.as_asgi(), name='chat')
                ]
            )
        ),
    ),
})
