# Generated by Django 4.1.7 on 2023-02-28 05:27

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0002_chatroom_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatroom',
            name='users',
            field=models.ManyToManyField(blank=True, related_name='chat_rooms', to=settings.AUTH_USER_MODEL),
        ),
    ]
