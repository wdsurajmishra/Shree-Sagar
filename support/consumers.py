from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import ChatMessage, SupportTicket
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.ticket_id = self.scope['url_route']['kwargs']['ticket_id']
        self.room_group_name = f"chat_{self.ticket_id}"

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
        data = json.loads(text_data)
        ticket_id = data['ticket_id']
        message = data['message']
        sender_id = data['sender_id']
        is_agent_message = data['is_agent_message']

        # Save the message
        ticket = SupportTicket.objects.get(id=ticket_id)
        sender = User.objects.get(id=sender_id)
        ChatMessage.objects.create(
            ticket=ticket,
            sender=sender,
            message=message,
            is_agent_message=is_agent_message,
        )

        # Send message to the room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_id': sender_id,
                'is_agent_message': is_agent_message,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender_id = event['sender_id']
        is_agent_message = event['is_agent_message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender_id': sender_id,
            'is_agent_message': is_agent_message,
        }))
