from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

from channelsApp import consumers

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter([  # channelsApp.routing.websocket_urlpatterns
            path('channels/<str:room_name>/', consumers.ChatConsumer), ]

        )
    ),
})
