from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime 


# User:  auth_user (contrib.auth.User)
#   user of Buzzer
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

# Profile: buzzer_profile

#   extension User (one to one)

class Profile (models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    screen_name = models.CharField(max_length=50)  # name that appears on screen (complementary username)
    location = models.CharField(max_length=150)  # defined location for user account’s profile
    url = models.CharField(max_length=150)  # URL provided by the user in association with their profile
    bio = models.CharField(max_length=150) # general information about user 
    birthday = models.DateField(auto_now=False, auto_now_add=False,null=True) # user's birthday
    image = models.ImageField(default='buzzer_logo.png',verbose_name='Image',upload_to='media',blank=True)
    def __str__(self):
        return(self.user.username + " - " + self.screen_name + " - " + self.user.first_name + " - " + self.user.last_name)


    def all_fields(self):
        data = self.all_fields_user()
        data += "  screen_name: " + self.screen_name        
        data += "  location: " + self.location
        data += "  url: " + self.url
        data += "  bio: " + self.bio
        data += "  birthday: " + str(self.birthday)
        data += "  image: " + str(self.image)
        return(data)


    def all_fields_user(self):
        data = "key: " + str(self.user.id)
        data += "  username: " + self.user.username + "  password: " + self.user.password
        data += " first name: " + self.user.first_name + " last name: " + self.user.last_name
        data += " email: " + self.user.email
        return data




# Buz: buzzer_buz
#   posts of buzzer
class Buzz (models.Model):
    id_buzz = models.AutoField(primary_key=True) # id of buzz: automatic incremental
    user = models.ForeignKey(User, on_delete=models.CASCADE) # id of user who creates the buzz
    text = models.TextField(max_length=140) # text of the buzz
    created_at = models.DateTimeField(default=datetime.now, blank=True) # creation date time
    published_date = models.DateTimeField(blank=True, null=True) # publication date time

    def __str__(self):
        #return(self.title)
        return(self.text[:10])
        
    def all_fields(self):        
        data = "id_buzz: " + str(self.id_buzz)
        data += "  id_user: " + str(self.user.id)
        data += "  text: " + self.text
        data += "  created_at: " + str(self.created_at)
        data += "  published_date: " + str(self.published_date)		
        return data

    def published(self):
        self.published_data = timezone.now()
        self.save()





