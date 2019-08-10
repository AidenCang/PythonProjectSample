from channels.generic.websocket import AsyncWebsocketConsumer
import json

from twisted.protocols.memcache import ClientError


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("connect")
        print(self.scope)
        self.room_group_name = None
        self.channel_name = None
        if self.scope['user'].is_anonymous:
            await self.accept()
            # Send a message down to the client
            await self.send(
                json.dumps({
                    "msg_type": "connect",
                    "room": self.scope['url_route']['kwargs']['room_name'],
                    "username": str(self.scope['user']),
                }),
            )
            await  self.close()
        else:
            self.room_name = self.scope['url_route']['kwargs']['room_name']
            self.room_group_name = 'chat_%s' % self.room_name

            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()

    async def disconnect(self, close_code):
        if self.room_group_name is not None and self.channel_name is not None:
            try:
                # Leave room group
                await self.channel_layer.group_discard(
                    self.room_group_name,
                    self.channel_name
                )
            except ClientError:
                pass

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
