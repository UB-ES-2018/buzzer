from channels.consumer import AsyncConsumer
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

        print("connected",event)
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
        print("received",event)
        front_text = event.get('text',None)
        if front_text is not None:
            dict_data = json.loads(front_text)
            msg = dict_data.get('message')
            user = self.scope['user']
            #NIBRASS: se consigue el nombre (str) i el objeto user
            other_username = self.scope['url_route']['kwargs']['user']
            other_user = User.objects.get(username=other_username)
            me = str(user)

            id = await self.get_id(me,other_username)
            #print(id.id_chat)
            # Guardamos
            save_msg = views.send_message(me,other_username,msg,notified='False')
            #save_noti = views.create_notification(msg, "", other_user, 1, message=msg, buzz=None, follower=None)
            print(save_msg)
            #print(save_noti)

            username = 'default'
            num_noti_sender = None;
            num_noti_reciver = None;
            if user.is_authenticated:
                username= user.username
                chat = views.look_for_new_messages(other_username)
                num_noti_sender = user.profile.count_notification;
                num_noti_reciver = other_user.profile.count_notification;
            # NIBRASS: se consigue el numero de notis

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

            """await self.send({
                "type": "websocket.send",
                "text": json.dumps(myResponse),
            })"""

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
        print("connected notification", event, )

        await self.send({
            "type": "websocket.accept"
        })
        pass

    async def websocket_receive(self,event):
        pass

    async def websocket_disconnect(self, event):
        print("disconnected", event)
