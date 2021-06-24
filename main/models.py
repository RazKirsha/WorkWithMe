from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

from offers.models import Skills

RATE_CHOICES = [
    (1, '1 - Horrible'),
    (2, '2 - just an amateur'),
    (3, '3 - Can get better'),
    (4, '4 - nah..'),
    (5, '5 - average at best'),
    (6, '6 - OK'),
    (7, '7 - kinda fine'),
    (8, '8 - Really good'),
    (9, '9 - Super great'),
    (10, '10 - A God'),
]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    skills = models.ManyToManyField(Skills, blank=True)
    picture = models.ImageField(upload_to='images/', default='images/default-profile-picture1.jpg')
    about = models.TextField(max_length=1000, default='Hello Worldie')
    rating = models.SmallIntegerField(choices=RATE_CHOICES, blank=True)
    created = models.DateTimeField(default=datetime.now())
    reviews_num = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.username

    @property
    def is_pro(self):
        return self.skills.all().exists()
