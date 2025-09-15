import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
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

    # Receive message from WebSocket
    async def receive(self, text_data):
        # Import models inside the method
        from .models import Message
        from django.contrib.auth.models import User
        
        data = json.loads(text_data)
        message = data['message']
        sender = data['sender']
        receiver = data['receiver']

        # 1️⃣ Database e save kora
        sender_user = await database_sync_to_async(User.objects.get)(username=sender)
        receiver_user = await database_sync_to_async(User.objects.get)(username=receiver)

        await database_sync_to_async(Message.objects.create)(
            sender=sender_user,
            receiver=receiver_user,
            content=message
        )

        # 2️⃣ Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender,
                'receiver': receiver,
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        receiver = event['receiver']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'receiver': receiver,
        }))