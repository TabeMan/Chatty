from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from .models import ChatMessage, ChatRoom
from django.contrib.auth.models import User


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_slug = self.scope['url_route']['kwargs']['room_slug']
        print(self.scope)
        self.room_group_name = 'chat_%s' % self.room_slug
        self.room = await sync_to_async(ChatRoom.objects.get)(slug=self.room_slug)

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        self.user = self.scope['user']

        await self.save_user(self.user, self.room)

        # Send message to all clients with the updated list of users
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_list',
                'users': await self.get_usernames(),
            }
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        await self.remove_user(self.user, self.room)

        # Send message to all clients with the updated list of users
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_list',
                'users': await self.get_usernames(),
            }
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']
        room = text_data_json['room']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'room': room,
            }
        )

        await self.save_message(message, username, room)

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        room = event['room']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'room': room,
        }))

    # Receive message from room group with the updated list of users
    async def user_list(self, event):
        users = event['users']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'users': users,
        }))

    @sync_to_async
    def save_message(self, message, username, room):
        user = User.objects.get(username=username)
        room = self.room
        ChatMessage.objects.create(
            user=user, room=room, message_content=message)

    @sync_to_async
    def save_user(self, user, room):
        room.users.add(user)

    @sync_to_async
    def remove_user(self, user, room):
        room.users.remove(user)

    @sync_to_async
    def get_usernames(self):
        return [user.profile.username for user in self.room.users.all()]
