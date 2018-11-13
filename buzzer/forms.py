from django import forms
from .models import Buzz,Profile


class PostForm(forms.ModelForm):
    class Meta :
        model = Buzz
        fields = ('text',)

class ProfileForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    class Meta :
        model = Profile
        fields = ('image',)