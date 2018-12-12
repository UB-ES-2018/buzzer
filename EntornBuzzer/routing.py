from channels.routing import ProtocolTypeRouter,URLRouter
from django.conf.urls import url
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator,OriginValidator

from buzzer.consumers import ChatConsumer, NotiConsumer,ProfileConsumer
application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
    'websocket':AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                [

                    url(r'^message/$', ChatConsumer),
                    url(r'^message/(?P<user>.*)/$', ChatConsumer),

                    url(r'^notify/$', NotiConsumer),
                    url(r'^notify/(?P<user>.*)/$', NotiConsumer),

                    url(r'^search/(?P<search_hastag>.*)/$', NotiConsumer),
                    url(r'^search/$', NotiConsumer),

                    url(r'^profile/(?P<user>.*)/$', ProfileConsumer),
                    url(r'^profile/$', NotiConsumer),

                ]
            )
        )
    )
})