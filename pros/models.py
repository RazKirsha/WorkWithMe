from django.db import models
from offers.models import Offers
from main.models import Profile
from datetime import datetime
import secrets


def gen_code():
    return secrets.token_urlsafe(20)


# Create your models here.
class AcceptOffer(models.Model):
    offer = models.OneToOneField(Offers, on_delete=models.CASCADE)
    pro = models.ForeignKey(Profile, on_delete=models.CASCADE)
    meeting_time = models.DateTimeField(default=datetime.now())
    seen = models.BooleanField(default=False)
    code = models.CharField(max_length=500, default=gen_code)
    updated = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    @property
    def reformat_time(self):
        offer_time = self.meeting_time
        new_time = offer_time.strftime("%Y-%m-%dT%H:%M:%S")
        return new_time
