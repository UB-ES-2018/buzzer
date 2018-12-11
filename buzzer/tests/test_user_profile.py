import json
from django.test import TestCase
from django.test import SimpleTestCase
from django.test import Client
from django.contrib.auth.models import User
from ..models import Profile,Buzz,Hashtag,Chat,Message,Follow,Notification
from ..views import loginView,signupView
from django.urls import reverse
 

# TEST FEATURE USER PROFILE (LOGIN,LOGOUT,ETC)

class YourTestClass(TestCase):

    @classmethod
    def setUpTestData(cls):
        # setUpTestData: Run once to set up non-modified data for all class methods
        print("Test Feature User-Profile (login,logout,etc)")
        user1 = User.objects.create(username='u1',password='psw1')           
        pass

    def setUp(self):
        # setUp: Run once for every test method to setup clean data
        pass
   
    
    def test_loginView(self):
        # test function login
        response = self.client.get('/buzzer/login/', {'username': 'us1', 'password': 'psw1'})
        self.assertEquals(200,response.status_code)
        pass 
       
    def test_loginViewError(self):
        # test function login with error in password
        response = self.client.get('/buzzer/login/', {'username': 'us1', 'password': ''})
        self.assertEquals(200,response.status_code)
        pass 
    
    def test_signupView(self):
        # test function signup
        response =  self.client.get('/buzzer/signup/', {'username': 'us2', 'password': 'psw2', 'name': 'name1', 'surname': 'surname1', 'email': 'email1', 'usertag': 'usertag1'})
        self.assertEquals(200,response.status_code)         
        pass 
     
