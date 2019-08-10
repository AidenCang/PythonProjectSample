from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

from channelsApp.chatconsumers import ChatRoomConsumer
from channelsApp.consumers import ChatConsumer

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter([
            path('channels/<str:room_name>/', ChatConsumer),
            path("chat/stream/", ChatRoomConsumer),
        ]

        )
    ),
})
