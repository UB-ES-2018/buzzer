from django.test import TestCase
from django.test import SimpleTestCase
from django.test import Client
from django.contrib.auth.models import User
from ..models import Chat,Message
from ..views import create_chat,create_message,search_chat,equal_list,messages_chat,equal_list

################################################################################
# TEST FEATURE SENDING MESSAGES 
################################################################################

class Test_Message(TestCase):

    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: create data in data base ")
        user1 = User.objects.create(username='u1',password='psw1')
        user2 = User.objects.create(username='u2',password='psw1')
        pass

    def setUp(self):
        #print("setUp: Run once for every test method to setup clean data.")
        pass

    def test_create_chat(self):
        print("Method: test_create_chat")
        user1 = User.objects.get(username='u1')
        user2 = User.objects.get(username='u2')
        chat = create_chat([user1,user2])
        self.assertEquals(chat.name,'u1u2')
        pass

    def test_search_chat(self):
        print("Method: test_search_chat")
        user1 = User.objects.get(username='u1')
        user2 = User.objects.get(username='u2')
        chat1 = create_chat([user1,user2])
        chat2 = search_chat(['u1','u2'])
        self.assertEquals(chat1.id_chat,chat2.id_chat)
        pass

    def test_create_message(self):
        print("Method: test_create_message")
        text_message = 'test1'
        user1 = User.objects.get(username='u1')
        user2 = User.objects.get(username='u2')
        list_of_users = [user1.username,user2.username]
        chat = search_chat(list_of_users)
        message = create_message(chat.id_chat,user1.username,text_message)
        self.assertEquals(message.content,'test1')
        self.assertEquals(message.user.username,'u1')
        pass

