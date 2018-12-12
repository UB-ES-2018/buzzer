from django.test import TestCase
from django.test import SimpleTestCase
from django.test import Client
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from ..models import Profile, Buzz, Hashtag, Chat, Message, Follow, Notification
from ..views import create_chat,post_new 

# TEST FEATURE SENDING BUZZS AND HASHTAGS

class Test_Message(TestCase):

    @classmethod
    def setUpTestData(self):
        # setUpTestData: Run once to set up non-modified data for all class methods
        print("Test Feature Sending Buzzs and Hashtags")
        user1 = User.objects.create(username='u1',password='psw1')
        user2 = User.objects.create(username='u2',password='psw1')
        authenticate(username='u1', password='psw1')
        pass

    def setUp(self):
        # setUp: Run once for every test method to setup clean data
        self.client = Client()
        pass
    
    def test_post_new(self):
        # test function post_new
        user1 = User.objects.get(username='u1')
        user2 = User.objects.get(username='u2')        
        response = self.client.post('/buzzer/new_post/', {'text': 'txt'})
        self.assertEquals(302,response.status_code)
        pass     
     
   



    
