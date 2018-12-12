from django.test import TestCase
from django.test import SimpleTestCase
from django.contrib.auth.models import User
from ..models import Profile,Buzz,Hashtag,Chat,Message,Follow,Notification

################################################################################
# TEST MODEL 
################################################################################

class Test_Model_Buzzer(TestCase):

    @classmethod
    
    def setUpTestData(cls):
        # setUpTestData (Run once to set up non-modified data for all class methods
        print("Test Model")
        pass

    def setUp(self):
        # setUp (Run once for every test method to setup clean data 
        pass
    
    def test_model_User(self):
        # test model User
        user = User.objects.create(username='username',password='psw',first_name = 'firstname',last_name = 'lastname')
        self.assertTrue(isinstance(user, User))
        pass        

    def test_model_Profile(self):
        # test model Profile
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
        "  image: " + str(profile.image) + 
        "  count_follower: " + str(profile.count_follower) +
        "  count_followed: " + str(profile.count_followed) +
        "  count_notification: " + str(profile.count_notification))
        pass

    def test_model_Buzz(self):
        # test model Buzz
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
        # test model Hashtag
        user = User(username='username',password='psw',first_name = 'firstname',last_name = 'lastname')
        buzz = Buzz(user=user,text='text')
        hashtag = Hashtag(text='text')
        self.assertTrue(isinstance(hashtag, Hashtag))
        self.assertEquals(str(hashtag),hashtag.text)
        pass

    def test_model_Chat(self):
        # test model Chat
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
        # test model Message
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
      
    def test_model_Follow(self):
        # test model Follow
        user1 = User(username='username1',password='psw1',first_name = 'firstname1',last_name = 'lastname1')
        user2 = User(username='username2',password='psw2',first_name = 'firstname2',last_name = 'lastname2')
        follow = Follow(follower=user1,followed=user2)
        self.assertTrue(isinstance(follow, Follow))
        self.assertEquals(str(follow),follow.follower.username + " follows " + follow.followed.username)
        self.assertEquals(follow.all_fields(),
        "follower: " + str(follow.follower) +
        "  followed: " + str(follow.followed) +
        "  created: " + str(follow.created) +
        "  rejected: " + str(follow.rejected))
        pass
        
    def test_model_Notification(self):  
        # test model Notification (of buzz)
        user1 = User(username='username1',password='psw1',first_name = 'firstname1',last_name = 'lastname1')
        buzz = Buzz(user=user1,text='text')
        notification = Notification(title='title',description='description',type_notification=2,user_notify=user1,buzz=buzz)
        self.assertTrue(isinstance(notification, Notification))
        self.assertEquals(str(notification),notification.title + " - " + notification.description)
        self.assertEquals(notification.all_fields(),
        "id_notification: " + str(notification.id_notification) +
        "  title: " + str(notification.title) +
        "  description: " + str(notification.description) +
        "  user_notify: " + str(notification.user_notify) +
        "  created: " + str(notification.created) +
        "  type_notification: " + str(notification.type_notification) +
        "  buzz: " + str(notification.buzz))
        pass
