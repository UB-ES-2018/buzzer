import json
from django.test import TestCase
from django.test import SimpleTestCase
from django.test import Client
from django.contrib.auth.models import User
from ..models import Profile,Buzz,Hashtag,Chat,Message
from ..views import loginView
 

# TEST FEATURE SENDING MESSAGES 

class YourTestClass(TestCase):

    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up non-modified data for all class methods.")
        user1 = User.objects.create(username='u1',password='psw1')
           
        pass

    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")
        pass
   

    def test_login(self):
        c = Client() 
        response = c.post('/buzzer/login/', {'username': 'us1', 'password': 'psw1'})
        print(response)
        self.assertEquals(200,response.status_code)
        response = c.post('/buzzer/login/', {'username': '', 'password': 'psw1'})
        print(response)
        self.assertEquals(200,response.status_code)       

        pass 

     
