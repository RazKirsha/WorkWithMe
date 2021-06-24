from django import forms
from .models import *
from django.forms import ModelForm, Select
from django.contrib.admin.widgets import FilteredSelectMultiple

from main.models import Profile


class OfferForm(forms.ModelForm):
    class Meta:
        model = Offers
        fields = ['date_deadline', 'field', 'title', 'content', 'duration']

        widgets = {
            'field': forms.SelectMultiple(attrs={'class': 'form-control'})}


class SkillsForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['skills', 'picture', 'about']
