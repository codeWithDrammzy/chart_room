from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django import forms
from django.forms.widgets import PasswordInput, TextInput

from .models import Room,User

class CreateUser(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginUser(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder': 'Password'}))


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields =  '__all__'
        exclude = ['host', 'participants']
    

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['avater',  'name' ,'username', 'email', 'bio' ] 
    
