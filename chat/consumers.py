import json
import re
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Room, Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Original room name from URL
        self.raw_room_name = self.scope['url_route']['kwargs']['room_name']
        
        # Sanitize for group name (no spaces or special characters)
        cleaned_name = re.sub(r'[^a-zA-Z0-9_.-]', '_', self.raw_room_name)
        self.room_group_name = f"room_{cleaned_name}"

        # Join group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.close()

    async def receive(self, text_data):
        data_json = json.loads(text_data)

        # Send to group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "send_message",
                "message": data_json
            }
        )

    async def send_message(self, event):
        data = event["message"]

        # Save to database
        await self.create_message(data)

        response = {
            "sender": data["sender"],
            "message": data["message"]
        }

        # Send to WebSocket
        await self.send(text_data=json.dumps({"message": response}))

    @database_sync_to_async
    def create_message(self, data):
        room = Room.objects.get(room_name=data["room_name"])

        if not Message.objects.filter(
            message=data["message"], sender=data["sender"]
        ).exists():
            Message.objects.create(
                room=room,
                message=data["message"],
                sender=data["sender"]
            )
