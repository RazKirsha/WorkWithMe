from django import forms
from .models import *
from django.forms.widgets import SplitDateTimeWidget

from main.models import Profile


class AcceptOfferForm(forms.ModelForm):
    class Meta:
        model = AcceptOffer
        fields = ['meeting_time']

    # meeting_date = forms.DateField(widget=SplitDateTimeWidget)


class CreateFeedbackForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['rating']
