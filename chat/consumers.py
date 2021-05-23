import asyncio
import json

from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model

from .models import Thread, DialogMessage, Chat, ChatMessage

User = get_user_model()


class DialogConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        # when the socket connects
        # self.kwargs.get("username")
        self.other_username = self.scope['url_route']['kwargs']['username']
        user = self.scope['user']
        thread_obj = await self.get_thread(user, self.other_username)
        self.cfe_chat_thread = thread_obj
        self.room_group_name = thread_obj.room_group_name  # group

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        self.rando_user = await self.get_name()
        await self.send({
            "type": "websocket.accept"
        })

    async def websocket_receive(self, event):  # websocket.receive
        message_data = json.loads(event['text'])
        # print()
        user = self.scope['user']
        username = avatar = "unknown"
        if user.is_authenticated:
            username = user.username
            avatar = user.get_avatar()
        message_data["user"] = username
        message_data["avatar"] = avatar
        created_message = await self.create_chat_message(user, message_data['msg'])
        message_data["datetime"] = created_message.timestamp.strftime("%d.%m.%y %H:%M")
        message_data["id"] = created_message.id
        final_message_data = json.dumps(message_data)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': final_message_data
            }
        )

    async def broadcast_message(self, event):
        await self.send({
            "type": "websocket.send",
            "text": json.dumps({'msg': "Loading data please wait...", 'user': 'admin'})
        })
        await asyncio.sleep(15)  ### chatbot? API -> another service --> response --> send
        await self.send({
            "type": "websocket.send",
            "text": event['message']
        })

    async def chat_message(self, event):
        await self.send({
            "type": "websocket.send",
            "text": event['message']
        })

    async def websocket_disconnect(self, event):
        # when the socket connects
        # print(event)
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    @database_sync_to_async
    def get_name(self):
        return User.objects.all()[0].username

    @database_sync_to_async
    def get_thread(self, user, other_username):
        return Thread.objects.get_or_new(user, other_username)[0]

    @database_sync_to_async
    def create_chat_message(self, user, message):
        thread = self.cfe_chat_thread
        return DialogMessage.objects.create(thread=thread, user=user, message=message)


# //|||||||||||||||\\
# || CHAT Consumer ||
# \\|||||||||||||||//
class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        # when the socket connects
        # self.kwargs.get("username")
        self.slug = self.scope['url_route']['kwargs']['slug']
        user = self.scope['user']
        chat_obj = await self.get_chat(self.slug)
        self.cfe_chat_thread = chat_obj
        self.room_group_name = chat_obj.room_group_name  # group

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        self.rando_user = await self.get_name()
        await self.send({
            "type": "websocket.accept"
        })

    async def websocket_receive(self, event):  # websocket.receive
        message_data = json.loads(event['text'])
        # print()
        user = self.scope['user']
        username = avatar = "unknown"
        if user.is_authenticated:
            username = user.username
            avatar = user.get_chat_ico()
            chat_color = user.get_color()
            url = user.get_absolute_url()
        message_data["user"] = username
        message_data["icon"] = avatar
        message_data["color"] = chat_color
        message_data["url"] = url
        created_message = await self.create_chat_message(user, message_data['msg'])
        message_data["datetime"] = created_message.timestamp.strftime("%d.%m.%y %H:%M")
        message_data["id"] = created_message.id
        final_message_data = json.dumps(message_data)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': final_message_data
            }
        )

    async def broadcast_message(self, event):
        await self.send({
            "type": "websocket.send",
            "text": json.dumps({'msg': "Loading data please wait...", 'user': 'admin'})
        })
        await asyncio.sleep(15)  ### chatbot? API -> another service --> response --> send
        await self.send({
            "type": "websocket.send",
            "text": event['message']
        })

    async def chat_message(self, event):
        await self.send({
            "type": "websocket.send",
            "text": event['message']
        })

    async def websocket_disconnect(self, event):
        # when the socket connects
        # print(event)
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    @database_sync_to_async
    def get_name(self):
        return User.objects.all()[0].username

    @database_sync_to_async
    def get_chat(self, slug):
        return Chat.objects.get(slug=slug)

    @database_sync_to_async
    def create_chat_message(self, user, message):
        chat = self.cfe_chat_thread
        return ChatMessage.objects.create(thread=chat, user=user, message=message)
