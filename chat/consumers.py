from django.forms.models import model_to_dict
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Room, User
from musics.models import Music
import json

class ChatConsumer(AsyncWebsocketConsumer):
  	
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = self.room_name
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
	# websocket 연결 종료 시 실행 
    async def disconnect(self, close_code):
        await self.delete_user(self.user.id)
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
	# 클라이언트로부터 메세지를 받을 시 실행
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json.get('action')
        username = text_data_json.get('username')
        message = text_data_json.get('message')
        if action == 'enter':
            room, user_count = await self.get_room_or_create(self.room_name)
            # room에 아무도 없다면
            if user_count == 0:
                user = await self.create_user(username, True, room)
            else:
                user = await self.create_user(username, False, room)
            self.user = user
            await self.send(text_data=json.dumps({
                'action': 'enter',
                'isHost': user.is_host,
                'userList': await self.get_user_list(self.room_name),
            }))
        elif action == 'message':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat.message',
                    'message': message,
                    'username': username,
                }
            )
        elif action == 'music':
            if self.user.is_host:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat.music',
                    }
                )
        else:
            pass
    
    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        # WebSocket 에게 메세지 전송
        await self.send(text_data=json.dumps({
            'action': 'message',
            'message': message,
            'author': username,
        }))

    async def chat_music(self, event):
        music = await self.get_random_music()
        await self.send(text_data=json.dumps({
            'action': 'music',
            'music': music,
        }))

    
    @database_sync_to_async
    def get_room_or_create(self, room_name):
        room = Room.objects.get_or_create(room_name=room_name)
        user_count = room[0].user_set.count()
        return (room[0], user_count)


    @database_sync_to_async
    def create_user(self, username, is_host, room):
        user = User(is_host=is_host, username=username, room=room)
        user.save()
        return user


    @database_sync_to_async
    def get_user(self, username):
        user = User.objects.get(username=username)
        return user
    
    @database_sync_to_async
    def get_user_list(self, room_name):
        room = Room.objects.get(room_name=room_name)
        user_list = [member for member in room.user_set.values()]
        return user_list
    

    @database_sync_to_async
    def delete_user(self, user_id):
        user = User.objects.get(pk=user_id)
        user.delete()
    
    @database_sync_to_async
    def get_random_music(self):
        music = Music.objects.order_by('?').first()
        return model_to_dict(music)