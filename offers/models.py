from django.db import models
from django.utils import timezone

from datetime import datetime


# from main.models import Profile


# Create your models here.
class Skills(models.Model):
    abilities = models.CharField(max_length=200)

    def __str__(self):
        return self.abilities


def two_more_days():
    return timezone.now() + timezone.timedelta(days=2)


class Offers(models.Model):
    date_init = models.DateTimeField(auto_now_add=True)
    date_deadline = models.DateTimeField(default=two_more_days)
    offer_maker = models.ForeignKey('main.Profile', on_delete=models.CASCADE)
    field = models.ManyToManyField(Skills)
    title = models.CharField(max_length=200)
    content = models.CharField(max_length=500)
    duration = models.PositiveIntegerField(default=0)
    accepted = models.BooleanField(default=False)

    @property
    def expired(self):
        if self.date_deadline > timezone.now():
            return True
        return False

    def __str__(self):
        return self.title
