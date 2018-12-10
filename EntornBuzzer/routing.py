from channels.routing import ProtocolTypeRouter,URLRouter
from django.conf.urls import url
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator,OriginValidator

from buzzer.consumers import ChatConsumer
application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
    'websocket':AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                [
                    # Search
                    url(r'^search/(?P<search_hastag>.*)/$', ChatConsumer),
                    url(r'^search/$', ChatConsumer),

                    # Extras
                    url(r'^new_post/$', ChatConsumer),
                    url(r'^profile/(?P<user>.*)/$', ChatConsumer),
                    url(r'^actualizarProfile/(?P<user>.*)/$', ChatConsumer),
                    url(r'^messages/$', ChatConsumer),
                    url(r'^message/$', ChatConsumer),
                    url(r'^message/(?P<user>.*)/$', ChatConsumer),

                    # Browser DBs
                    url(r'^users/$', ChatConsumer),
                    url(r'^users/(?P<user>.*)/$', ChatConsumer),
                    url(r'^profiles/$', ChatConsumer),
                    url(r'^profiles/(?P<user>.*)/$', ChatConsumer),
                    url(r'^buzzs/$', ChatConsumer),
                    url(r'^buzzs/(?P<user>.*)/$', ChatConsumer),
                    url(r'^upload/$', ChatConsumer),

                    url(r'^notify/$', ChatConsumer),

                ]
            )
        )
    )
})