from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
from django.db.models import Q



# User:  auth_user (contrib.auth.User)
#   user of Buzzer
#
#   attributes of User:
#     id (integer- primary key - autoincrement)
#     username (varchar(128) - not null)
#     first_name (varchar(30) - not null)
#     last_name (varchar(150) . not null)
#     email (varchar(254) - not null)
#     password (varchar(128) - not null)
#     is_staff (boolean - not null)
#     is_active (boolean - not null)
#     is_superuser (boolean - not null)
#     last_login (datetime - null)
#     date_joined (datetime - null)
#
#     Profile: buzzer_profile
#       extension User (one to one)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    screen_name = models.CharField(max_length=50)  # name that appears on screen (complementary username)
    location = models.CharField(max_length=150)  # defined location for user account’s profile
    url = models.CharField(max_length=150)  # URL provided by the user in association with their profile
    bio = models.CharField(max_length=150) # general information about user 
    birthday = models.DateField(auto_now=False, auto_now_add=False,null=True) # user's birthday
    image = models.ImageField(default='media/buzzer_logo.png',verbose_name='Image',upload_to='media') # image user profile
    count_follower = models.PositiveIntegerField(default=0) # number of users follows me  
    count_followed = models.PositiveIntegerField(default=0) # number of users that I follow
    count_notification = models.PositiveIntegerField(default=0) # number of notifications pending (to be showed)    

    def __str__(self):
        return(self.user.username + " - " + self.screen_name + " - " + self.user.first_name + " - " + self.user.last_name)

    def __str__(self):
        return self.user.username + " - " + self.screen_name + " - " + self.user.first_name + " - " + self.user.last_name

    def all_fields(self):
        data = self.all_fields_user()
        data += "  screen_name: " + self.screen_name
        data += "  location: " + self.location
        data += "  url: " + self.url
        data += "  bio: " + self.bio
        data += "  birthday: " + str(self.birthday)
        data += "  image: " + str(self.image)
        data += "  count_follower: " + str(self.count_follower)
        data += "  count_followed: " + str(self.count_followed)
        data += "  count_notification: " + str(self.count_notification)
        return data

    def all_fields_user(self):
        data = "key: " + str(self.user.id)
        data += "  username: " + self.user.username + "  password: " + self.user.password
        data += " first name: " + self.user.first_name + " last name: " + self.user.last_name
        data += " email: " + self.user.email
        return data

    def get_follows(self): # return all follow-relationships (as follower and as followed)
        return Follow.objects.filter(Q(follower=self.user) | Q(followed=self.user))
        
    def get_followeds(self):
        followeds = []
        for follow in Follow.objects.filter(follower=self.user):
            followeds.append(follow.followed)
        return followeds  

    def get_followers(self):
        followers = []
        for follow in Follow.objects.filter(followed=self.user):
            followers.append(follow.follower)
        return followers

            
    


# Buz: buzzer_buz
#   posts of buzzer
class Buzz(models.Model):
    id_buzz = models.AutoField(primary_key=True)  # id of buzz: automatic incremental
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # id of user who creates the buzz
    text = models.TextField(max_length=140)  # text of the buzz
    created_at = models.DateTimeField(default=datetime.now, blank=True)  # creation date time
    published_date = models.DateTimeField(blank=True, null=True)  # publication date time
    file = models.FileField(verbose_name='Buzz File', upload_to='buzzfile', blank=True)
    file_type = models.CharField(max_length=100)

    def __str__(self):

        return self.text[:10]

    def all_fields(self):
        data = "id_buzz: " + str(self.id_buzz)
        data += "  id_user: " + str(self.user.id)
        data += "  text: " + self.text
        data += "  created_at: " + str(self.created_at)
        data += "  published_date: " + str(self.published_date)
        data += "  attached file: " + str(self.file)

        return data

    def published(self):
        self.published_data = timezone.now()
        self.save()

        
# Hashtag: buzzer_hashtag
#    hashtag of buzz
class Hashtag (models.Model):
     text = models.TextField(max_length=140,primary_key=True) # text of the hashtag (is key)
     buzzs = models.ManyToManyField(Buzz) # list of buzz of hashtag

     def __str__(self):
         return(self.text)

# Chat: chat_buzzer
#    chat of a set of users
class Chat (models.Model):
    id_chat = models.AutoField(primary_key=True)  # id of chat: automatic incremental
    name = models.CharField(max_length=50) # name of chat (default name: name of all members)
    members = models.ManyToManyField(User, blank=True) # all users of chat

    def __str__(self):
        return(self.name)

    def __eq__(self,other):
        equals = True
        for member in self.members:
            if member not in other.members:
                equals = False
                break 
 
        return equals    

    def all_fields(self):     
        data = "id_chat: " + str(self.id_chat)
        data += "  name: " + str(self.name)
        for member in self.members.all(): 
            data += "  user: " + str(member)
        
        return data
  

# Message: message_buzzer
#    message between users
class Message (models.Model):
    id_message = models.AutoField(primary_key=True)  # id of message: automatic incremental
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE) # sender of message (receiver are all users in chat)
    date = models.DateTimeField(blank=True, null=True) # date-time message sended
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE) # chat 
    content = models.CharField(max_length=140) # text of message
    notified = models.BooleanField(default=False)


    def __str__(self):
        return(self.content)	

    def all_fields(self):     
        data = "id_msg: " + str(self.id_message)
        data += "  user: " + str(self.user)
        data += "  date: " + str(self.date)
        data += "  chat: " + str(self.chat)
        data += "  content: " + str(self.content)
        data += "  notified: " + str(self.notified)
                 
        return data

# Follow: follow_buzzer
#    follower follows followed
class Follow (models.Model):
    follower = models.ForeignKey(User, related_name="who_is_followed", on_delete=models.CASCADE) # user who follows
    followed = models.ForeignKey(User, related_name="who_follows",on_delete=models.CASCADE) # user who is followed
    created = models.DateTimeField(auto_now_add=True, db_index=True) # date of creation of relationship
    rejected = models.DateTimeField(blank=True, null=True) # date of cancelation of relationship
      
    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return(self.follower.username + " follows " + self.followed.username)

    def all_fields(self):     
        data = "follower: " + str(self.follower)
        data += "  followed: " + str(self.followed)
        data += "  created: " + str(self.created)
        data += "  rejected: " + str(self.rejected)
        return data
      

# Notification: notification_buzzer
#    notification when there is a new message, buzz or follower
class Notification (models.Model):
    id_notification = models.AutoField(primary_key=True)  # id of notification: automatic incremental
    title = models.TextField(max_length=140) # title of notification
    description = models.TextField(max_length=140) # description of notification
    user_notify = models.ForeignKey(User, related_name="who_is_notified", null=True, on_delete=models.CASCADE) # all users to be notified    
    created = models.DateTimeField(auto_now_add=True, db_index=True) # date of creation of notification
    showed = models.BooleanField(default=False) # weather notification is showed
    type_notification = models.PositiveIntegerField(default=0) # notification type: 0-generic,1-message,2-buzz,3-follower
    message = models.ForeignKey(Message, null=True, on_delete=models.CASCADE) # notification of message
    buzz = models.ForeignKey(Buzz, null=True, on_delete=models.CASCADE) # notification of buzz
    follower = models.ForeignKey(User, related_name="follower", null=True, on_delete=models.CASCADE) # notificacion of follower 

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return(self.title + " - " + self.description)

    def all_fields(self):     
        data = "id_notification: " + str(self.id_notification)
        data += "  title: " + str(self.title)
        data += "  description: " + str(self.description)
        data += "  user_notify: " + str(self.user_notify)
        data += "  created: " + str(self.created)
        data += "  type_notification: " + str(self.type_notification)
        if self.type_notification == 1: 
            data += "  message: " + str(self.message)
        else:
            if self.type_notification == 2: 
                data += "  buzz: " + str(self.buzz)
            else:
                data += "  follower: " + str(self.follower)
        return data
