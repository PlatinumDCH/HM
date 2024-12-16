from django.db import models
from django.contrib.auth.models import User
from crv.quotes.models import Quotes


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    added_quotes = models.ManyToManyField(Quotes, related_name='added_by', blank=True)