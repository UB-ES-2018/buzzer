from django.test import TestCase
from django.test import SimpleTestCase
from django.test import Client
from django.contrib.auth.models import User
from ..models import Profile, Buzz, Hashtag, Chat, Message, Follow, Notification
from ..views import search_chat,create_message,create_notification,search_notifications
# TEST FEATURE NOTIFICATIONS 

class Test_Message(TestCase):

    @classmethod
    def setUpTestData(cls):
        # setUpTestData: Run once to set up non-modified data for all class methods
        user1 = User.objects.create(username='u1',password='psw1')
        profile1 = Profile.objects.create(user=user1)
        user2 = User.objects.create(username='u2',password='psw1')
        profile2 = Profile.objects.create(user=user2)
        pass

    def setUp(self):
        # setUp: Run once for every test method to setup clean data
        pass  
    
    def test_create_notification(self):
        # test function create_notification
        text_message = 'test1'
        user1 = User.objects.get(username='u1')
        user2 = User.objects.get(username='u2')
        list_of_users = [user1.username,user2.username]
        chat = search_chat(list_of_users)
        message1 = create_message(chat.id_chat,user1.username,text_message)
        create_notification("message", "of  " + user1.username, user2, 1,message1,None,None)
        notification = Notification.objects.get(id_notification=1)
        self.assertEquals(notification.user_notify.username,'u2')
        pass
    
    def test_search_notifications(self):
        # test function search_notifications
        text_message = 'test1'
        user1 = User.objects.get(username='u1')
        user2 = User.objects.get(username='u2')
        list_of_users = [user1.username,user2.username]
        chat = search_chat(list_of_users)
        message1 = create_message(chat.id_chat,user1.username,text_message)
        create_notification("message", "of  " + user1.username, user2, 1,message1,None,None)
        list_of_notifications = search_notifications(user2)
        self.assertEquals(list_of_notifications[0].user_notify.username,'u2')
        pass
   
