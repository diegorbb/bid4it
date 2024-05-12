from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm

from .models import *


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'password1', 'password2']