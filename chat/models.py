from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from channels.db import database_sync_to_async


class ChatRoom(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    users = models.ManyToManyField(User, related_name='chat_rooms', blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('chat:room', args=[self.slug])


class ChatMessage(models.Model):
    room = models.ForeignKey(
        ChatRoom, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_messages')
    message_content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} - {self.room.name} - {self.message_content}'
