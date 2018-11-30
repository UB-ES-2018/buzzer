from django import forms
from .models import Buzz,Profile, Message
from django.contrib.auth.models import User

#Formulario para inseratr un buzz con o sin imagen
class PostForm(forms.ModelForm):
    file = forms.FileField(required=False)

    class Meta:
        model = Buzz
        fields = ('text', 'file', )


#Formulario para mensajes privados
class PMessageForm(forms.ModelForm):
    content = forms.CharField(max_length=140, required=True, widget=forms.Textarea(attrs={'class': 'pmessage-input'}))

    class Meta:
        model = Message
        fields = ('content', )

#Formulario para cambiar la imagen de perfil
class ProfileForm(forms.ModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ('image',)

#Formulario para cambiar la informacion de perfil
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