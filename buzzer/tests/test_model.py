from django.test import TestCase
from django.test import SimpleTestCase
from django.contrib.auth.models import User
from ..models import Profile,Buzz,Hashtag,Chat,Message

################################################################################
# TEST MODEL 
################################################################################

class Test_Model_Buzzer(TestCase):

    @classmethod
    
    def setUpTestData(cls):
        # print("setUpTestData (Run once to set up non-modified data for all class methods)")
        pass

    def setUp(self):
        # print("setUp (Run once for every test method to setup clean data)")
        pass
    
    def test_model_User(self):
        print("Method: model User")
        user = User.objects.create(username='username',password='psw',first_name = 'firstname',last_name = 'lastname')
        self.assertTrue(isinstance(user, User))
        pass        

    def test_model_Profile(self):
        print("Method: model Profile")
        user = User(username='username',password='psw',first_name = 'firstname',last_name = 'lastname')
        profile = Profile(user=user)
        profile.screen_name = 'screename'
        self.assertTrue(isinstance(profile, Profile))
        self.assertEquals(str(profile),profile.user.username + " - " + profile.screen_name +
              " - " + profile.user.first_name + " - " + profile.user.last_name)
        self.assertEquals(profile.all_fields(), profile.all_fields_user() +
        "  screen_name: " + profile.screen_name +
        "  location: " + profile.location + 
        "  url: " + profile.url +
        "  bio: " + profile.bio +
        "  birthday: " + str(profile.birthday) +
        "  image: " + str(profile.image))
        pass

    def test_model_Buzz(self):
        print("Method: model Buzz")
        user = User(username='username',password='psw',first_name = 'firstname',last_name = 'lastname')
        buzz = Buzz(user=user,text='text')
        self.assertTrue(isinstance(buzz, Buzz))
        self.assertEquals(str(buzz),buzz.text[:10])
        self.assertEquals(buzz.all_fields(),
        "id_buzz: " + str(buzz.id_buzz) +
        "  id_user: " + str(buzz.user.id) +
        "  text: " + buzz.text +
        "  created_at: " + str(buzz.created_at) +
        "  published_date: " + str(buzz.published_date) +
        "  attached file: " + str(buzz.file))
        pass
        
    def test_model_Hashtag(self):
        print("Method: model Hashtag")
        user = User(username='username',password='psw',first_name = 'firstname',last_name = 'lastname')
        buzz = Buzz(user=user,text='text')
        hashtag = Hashtag(text='text')
        self.assertTrue(isinstance(hashtag, Hashtag))
        self.assertEquals(str(hashtag),hashtag.text)
        pass

    def test_model_Chat(self):
        print("Method: model Chat")
        user1 = User(username='username1',password='psw1',first_name = 'firstname1',last_name = 'lastname1')
        user2 = User(username='username2',password='psw2',first_name = 'firstname2',last_name = 'lastname2')
        chat = Chat(id_chat=1,name=user1.username+user2.username)
        self.assertTrue(isinstance(chat, Chat))
        self.assertEquals(str(chat),chat.name)
        self.assertEquals(chat.all_fields(),
        "id_chat: " + str(chat.id_chat) +
        "  name: " + str(chat.name))
        pass

    def test_model_Message(self):
        print("Method: model Message")
        user1 = User(username='username1',password='psw1',first_name = 'firstname1',last_name = 'lastname1')
        user2 = User(username='username2',password='psw2',first_name = 'firstname2',last_name = 'lastname2')
        chat = Chat(id_chat=1,name=user1.username+user2.username)
        message = Message(user=user1,chat=chat,content='text')
        self.assertTrue(isinstance(message, Message))
        self.assertEquals(str(message),message.content)
        self.assertEquals(message.all_fields(),
        "id_msg: " + str(message.id_message) +
        "  user: " + str(message.user) +
        "  date: " + str(message.date) +
        "  chat: " + str(message.chat) +
        "  content: " + str(message.content) +
        "  notified: " + str(message.notified))
        pass
      
           
        
  

      
        
        

     
        

     
      

