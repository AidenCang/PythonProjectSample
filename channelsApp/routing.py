# chat/routing.py
from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('channels/<str:room_name>/$', consumers.ChatConsumer),
]
