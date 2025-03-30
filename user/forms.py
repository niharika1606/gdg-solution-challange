from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    avatar = forms.ChoiceField(
    widget=forms.RadioSelect
    )
    class Meta:
        model = User
        fields = ['avatar','username', 'email', 'password1', 'password2']
       

