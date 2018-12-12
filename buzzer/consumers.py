from channels.consumer import AsyncConsumer
from django.db.models.signals import post_save
from django.dispatch import receiver
import asyncio
import json
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async

from .models import Chat,Message
from . import views
from .models import Profile, Buzz, Hashtag, Message, Chat, Follow, Notification
from django.contrib.auth.models import User

class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self,event):

        print("connected chat",event)
        other_user = self.scope['url_route']['kwargs']['user']
        me = self.scope['user']
        me = str(me)
        thread_obj = await self.get_id(me,other_user)
        chat_room = f"thread_{thread_obj.id_chat}"
        self.chat_room = chat_room
        await self.channel_layer.group_add(
            chat_room,
            self.channel_name
        )
        #print(other_user,me)
        # Send something to frontend
        # Accept the connection
        await self.send({
            "type": "websocket.accept"
        })
    async def websocket_receive(self,event):
        print("received chat",event)
        front_text = event.get('text',None)
        if front_text is not None:
            dict_data = json.loads(front_text)
            text = dict_data.get('message')
            tipo = dict_data.get('type')
            if tipo == 'msg':
                print('msg')
                dict_data = json.loads(front_text)
                msg = dict_data.get('message')
                user = self.scope['user']
                other_username = self.scope['url_route']['kwargs']['user']
                other_user = User.objects.get(username=other_username)
                me = str(user)
                print(me)
                id = await self.get_id(me,other_username)
                save_msg = views.send_message(me,other_username,msg,notified='False')

                username = 'default'
                num_noti_sender = None
                num_noti_reciver = None
                if user.is_authenticated:
                    username= user.username
                    num_noti_sender = user.profile.count_notification
                    num_noti_reciver = other_user.profile.count_notification

                myResponse = {
                    'message': msg,
                    'username':username,
                    'num_sender': num_noti_sender,
                    'num_reciver': num_noti_reciver,

                }
                await self.channel_layer.group_send(
                    self.chat_room,
                    {
                        "type": "chat_message",
                        "text": json.dumps(myResponse)
                    }
                )
            else:
                print('noti')
                user = self.scope['user']
                me = str(user)
                username = 'default'
                num_noti_sender = None

                if user.is_authenticated:
                    username = user.username
                    num_noti_sender = user.profile.count_notification

                myResponse = {
                    'username': username,
                    'num_sender': num_noti_sender,

                }

                await self.send({
                    "type": "websocket.send",
                    "text": json.dumps(myResponse)
                })


    async def chat_message(self,event):

        await self.send({
            "type": "websocket.send",
            "text": event['text'],
        })

    async def websocket_disconnect(self, event):
        print("disconnected", event)

    async def get_id(self,me,other_username):
        return views.search_chat([me,other_username])



class NotiConsumer(AsyncConsumer):
    async def websocket_connect(self,event):
        print("connected notification", event)
        await self.send({
            "type": "websocket.accept"
        })
        user = self.scope['user']
        me = str(user)
        thread_obj = await self.get_id(me)
        notification_change = f"thread_{thread_obj.profile.count_notification}"
        myResponse = {
            'username': me,
            'num_sender': user.profile.count_notification,

        }
        await self.send({
            "type": "websocket.send",
            "text": json.dumps(myResponse)
        })

    async def websocket_receive(self,event):
        #print("received notification", event)
        user = self.scope['user']
        me = str(user)
        print(me)
        username = 'default'
        num_noti_sender = None

        if user.is_authenticated:
            username = user.username
            num_noti_sender = user.profile.count_notification

        myResponse = {
            'username': username,
            'num_sender': num_noti_sender,

        }

        await self.send({
            "type": "websocket.send",
            "text": json.dumps(myResponse)
        })
    async def websocket_disconnect(self, event):
        print("disconnected", event)

    async def get_id(self,me):
        return views.search_notify(me)



class ProfileConsumer(AsyncConsumer):
    async def websocket_connect(self,event):
        print("connected profile", event)
        await self.send({
            "type": "websocket.accept"
        })
        user = self.scope['user']
        me = str(user)
        print(me)

        myResponse = {
            'username': me,
            'num_sender': user.profile.count_notification,

        }
        await self.send({
            "type": "websocket.send",
            "text": json.dumps(myResponse)
        })

    async def websocket_receive(self,event):
        #print("received profile", event)
        user = self.scope['user']
        me = str(user)
        print(me)
        username = 'default'
        num_noti_sender = None
        if user.is_authenticated:
            username = user.username
            num_noti_sender = user.profile.count_notification
        #print(num_noti_sender)
        myResponse = {
            'username': username,
            'num_sender': num_noti_sender,

        }

        await self.send({
            "type": "websocket.send",
            "text": json.dumps(myResponse)
        })
    async def websocket_disconnect(self, event):
        print("disconnected", event)

    async def get_id(self,me):
        return views.search_notify(me)
