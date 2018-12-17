from django.test import TestCase
from django.test import SimpleTestCase
from django.test import Client
from django.contrib.auth.models import User
from ..models import Profile, Buzz, Hashtag, Chat, Message, Follow, Notification
from ..views import create_chat,create_message,search_chat,equal_list,messages_chat

# TEST FEATURE SENDING MESSAGES 

class Test_Message(TestCase):

    @classmethod
    def setUpTestData(cls):
        # setUpTestData: Run once to set up non-modified data for all class methods
        print("Test Feature Sending Messages")
        user1 =User.objects.create(username='u1',password='psw1')
        user2 = User.objects.create(username='u2',password='psw1')
        pass

    def setUp(self):
        # setUp: Run once for every test method to setup clean data
        pass

    def test_create_chat(self):
        # test function create_chat")
        user1 = User.objects.get(username='u1')
        user2 = User.objects.get(username='u2')
        list_of_users = [user1,user2]
        chat = create_chat(list_of_users)
        self.assertEquals(chat.name,'u1u2')
        pass

    
    def test_search_chat(self):
        # test function search_chat")
        user1 = User.objects.get(username='u1')
        user2 = User.objects.get(username='u2')
        chat = search_chat(['u1','u2'])
        list_of_users = []
        for user in chat.members.all():
            list_of_users.append(user.username)  	
        self.assertEquals(list_of_users,['u1','u2'])
        pass
    

    def test_create_message(self):
        # test function create_message")
        text_message = 'test1'
        user1 = User.objects.get(username='u1')
        user2 = User.objects.get(username='u2')
        list_of_users = [user1.username,user2.username]
        chat = search_chat(list_of_users)
        message = create_message(chat.id_chat,user1.username,text_message)
        self.assertEquals(message.content,'test1')
        self.assertEquals(message.user.username,'u1')
        pass

    """
    def test_profilePost(self):
        user1 = User.objects.get(username='u1')
        user2 = User.objects.get(username='u2')
        list_of_users = [user1.username,user2.username]
        chat = search_chat(list_of_users)
        response = self.client.get('/buzzer/profiles/', {'method': 'POST', 'user': 1, 'chat': 1, 'content': 'txt'})
        print(response)
        self.assertEquals(200,response.status_code)
        pass 
    """
        
      

