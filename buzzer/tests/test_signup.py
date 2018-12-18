import json
from django.test import TestCase
from django.test import SimpleTestCase
from django.test import Client
from django.contrib.auth.models import User
from ..models import Profile,Buzz,Hashtag,Chat,Message
from ..views import loginView,signupView
 
################################################################################
# TEST FEATURE SIGNUP
################################################################################
class Test_Signup(TestCase):

    @classmethod
    def setUpTestData(cls):
        print("Testing Signup...") # Run once to set up non-modified data for all class methods            
        pass
    
    def test_signup(self):
        c = Client() 

        response = c.get('/buzzer/signup/', follow=True)
        self.assertEquals(200,response.status_code)

        user_data = {
            'username': 'u1',
            'password': 'psw1',
            'name': 'Usuario',
            'surname': 'De prueba',
            'email': 'user1@user1.com',
            'usertag': 'el_usuario'
        }

        response = c.post('/buzzer/signup/', user_data , follow=True)
        self.assertEquals(200,response.status_code)
        self.assertTrue(response.context['user'].is_authenticated)

        user = response.context['user']

        self.assertEquals('u1', user.username)
        self.assertEquals('Usuario', user.first_name)
        self.assertEquals('De prueba', user.last_name)
        self.assertEquals('user1@user1.com', user.email)
        self.assertEquals('el_usuario', user.profile.screen_name)

        c.logout()
        pass