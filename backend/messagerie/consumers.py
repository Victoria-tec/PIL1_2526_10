import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Conversation, Message

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.room_group_name = f'chat_{self.conversation_id}'

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

    async def receive(self, text_data):
        data = json.loads(text_data)
        contenu = data['contenu']
        user = self.scope['user']

        message = await self.sauvegarder_message(user, contenu)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': contenu,
                'expediteur': user.get_full_name() or user.username,
                'envoye_le': message.envoye_le.strftime('%H:%M'),
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'expediteur': event['expediteur'],
            'envoye_le': event['envoye_le'],
        }))

    @database_sync_to_async
    def sauvegarder_message(self, user, contenu):
        conversation = Conversation.objects.get(id=self.conversation_id)
        return Message.objects.create(
            conversation=conversation,
            expediteur=user,
            contenu=contenu
        )
