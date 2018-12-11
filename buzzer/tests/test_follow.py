from django.test import TestCase
from django.test import SimpleTestCase
from django.test import Client
from django.contrib.auth.models import User
from ..models import Profile, Buzz, Hashtag, Chat, Message, Follow, Notification
from ..views import new_follow,new_follow_usernames,search_follows,search_followers,search_followeds

# TEST FEATURE FOLLOW (FOLLOWER)

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
    
    def test_new_follow(self):
        # test function new_follow
        user1 = User.objects.get(username='u1')
        user2 = User.objects.get(username='u2')         
        follow = new_follow(user1,user2)
        self.assertEquals(follow.follower.username+follow.followed.username,'u1u2')
        pass
    
    def test_new_follow_usernames(self):
        # test function new_follow_usernames             
        follow = new_follow_usernames('u1','u2')
        self.assertEquals(follow.follower.username+follow.followed.username,'u1u2')
        pass
    
    def test_search_follows(self):
        # test function search_follows   
        user1 = User.objects.get(username='u1')
        user2 = User.objects.get(username='u2')         
        follow = new_follow(user1,user2)          
        list_of_follows = search_follows('u1')
        self.assertEquals(list_of_follows[0].followed.username,'u2')
        pass
    
    def test_search_followers(self):
        # test function search_followers 
        user1 = User.objects.get(username='u1')
        user2 = User.objects.get(username='u2')         
        follow = new_follow(user1,user2)          
        list_of_followers = search_followers('u2')
        self.assertEquals(list_of_followers[0].username,'u1')
        pass
 
    def test_search_followeds(self):
        # test function search_followeds 
        user1 = User.objects.get(username='u1')
        user2 = User.objects.get(username='u2')         
        follow = new_follow(user1,user2)          
        list_of_followeds = search_followeds('u1')
        self.assertEquals(list_of_followeds[0].username,'u2')
        pass

     
