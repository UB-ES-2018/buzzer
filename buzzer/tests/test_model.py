from django.test import TestCase
from django.test import SimpleTestCase
from django.contrib.auth.models import User
from ..models import Profile,Hashtag,Chat,Message
from ..views import create_chat,create_message,search_chat,equal_list

# TEST FEATURE SENDING MESSAGES 

class BuzzerModelTest(TestCase):

    @classmethod
    
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up non-modified data for all class methods.")
        user1 =User.objects.create(username='u1',password='psw1')
        user2 = User.objects.create(username='u2',password='psw1')
        list_of_users = [user1,user2]
        chat = create_chat(list_of_users)
        pass


    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")
        pass
    
    def test_create_user_and_profile(self):
        print("create user and profile")
        user1 = User.objects.create(username='username',password='psw1')
        user1.first_name = 'firstname'
        user1.last_name = 'lastname'
        profile1 = Profile(user=user1)
        profile1.screen_name = 'screename1'
        return user1,profile1        

    def test_create_chat(self):
        print("Method: test_user")
        user1,profile1 = self.create_user()
        self.assertTrue(isinstance(user1, User))
        self.assertEquals(user1.username,str(user1))
        self.assertEquals(str(profile1),profile1.user.username + " - " + profile1.screen_name +
              " - " + profile1.user.first_name + " - " + profile1.user.last_name)
        self.assertEquals(profile1.all_fields(), profile1.all_fields_user() +
        "  screen_name: " + profile1.screen_name +
        "  location: " + profile1.location + 
        "  url: " + profile1.url +
        "  bio: " + profile1.bio +
        "  birthday: " + str(profile1.birthday) +
        "  image: " + str(profile1.image))


        pass

     
      

