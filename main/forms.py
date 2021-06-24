from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm


class CustomCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


