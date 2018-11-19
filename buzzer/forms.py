from django import forms
from .models import Buzz,Profile
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
    file = forms.FileField(required=False)

    class Meta:
        model = Buzz
        fields = ('text', 'file', )


class ProfileForm(forms.ModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ('image',)


class Profile2Form(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=150, required=False)
    email = forms.EmailField(required=False)
    screen_name = forms.CharField(max_length=50, required=False)  # name that appears on screen (complementary username)
    location = forms.CharField(max_length=150, required=False)  # defined location for user account’s profile
    url = forms.CharField(max_length=150, required=False)  # URL provided by the user in association with their profile
    bio = forms.CharField(max_length=150, required=False)  # general information about user
    birthday = forms.DateField(required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email','screen_name', 'location', 'url', 'bio', 'birthday')
