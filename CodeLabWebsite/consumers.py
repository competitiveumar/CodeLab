import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'global'  # Use a common room name
        self.room_group_name = f'chat_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message')
        file = text_data_json.get('file')
        filename = text_data_json.get('filename')
        audio = text_data_json.get('audio')
        user = self.scope["user"]
        sender_name = user.username if user.is_authenticated else "Anonymous"

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'file': file,
                'filename': filename,
                'audio': audio,
                'sender': sender_name
            }
        )

    async def chat_message(self, event):
        message = event.get('message')
        file = event.get('file')
        filename = event.get('filename')
        audio = event.get('audio')
        sender = event['sender']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'file': file,
            'filename': filename,
            'audio': audio,
            'sender': sender
        }))