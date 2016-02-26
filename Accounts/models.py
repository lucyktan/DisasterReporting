from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Account(models.Model):
	user = models.OneToOneField(User)
	email = models.EmailField(default='Email Address')
	first_name = models.CharField(default='First Name')
	last_name = models.CharField(default='Last Name')