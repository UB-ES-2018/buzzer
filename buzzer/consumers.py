from channels.consumer import AsyncConsumer
import asyncio
import json
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async

from .models import Chat,Message
from . import views
class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self,event):

        print("connected",event)

        other_user = self.scope['url_route']['kwargs']['user']
        me = self.scope['user']
        me = str(me)
        thread_obj = await self.get_id(me,other_user)
        chat_room = f"thread_{thread_obj.id_chat}"
        self.chat_room = chat_room
        """await self.channel_layer.group_add(
            chat_room,
            self.channel_name
        )"""
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
            other_user = self.scope['url_route']['kwargs']['user']
            me = str(user)
            #print(user,other_user,type(me),type(other_user))
            id = await self.get_id(me,other_user)
            #print(id.id_chat)
            #save_msg = views.send_message(me,other_user,msg,notified='False')
            #print(save_msg)
            username = 'default'
            if user.is_authenticated:
                username= user.username
                chat = views.look_for_new_messages(other_user)
                #print(chat)
                num_noti= len(chat)


            myResponse = {
                'message': msg,
                'username':username,
                'num':num_noti

            }
            """await self.channel_layer.group_send(
                self.chat_room,
                {
                    "type": "chat_message",
                    "text": json.dumps(myResponse)
                }
            )"""

            await self.send({
                "type": "websocket.send",
                "text": json.dumps(myResponse),
            })

    async def chat_message(self,event):
        await self.send({
            "type": "websocket.send",
            "text":event['text']
        })

    async def websocket_disconnect(self, event):
        print("disconnected", event)

    async def get_id(self,me,other_user):
        return views.search_chat([me,other_user])