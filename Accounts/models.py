from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

""" The Account model takes user information from the user_auth table
and will match it with the reports table """

class Account(models.Model):
	user = models.OneToOneField(User,to_field='username',unique=True)
	email = models.EmailField(max_length=50, default='Email Address')
	first_name = models.CharField(max_length=50, default='First Name')
	last_name = models.CharField(max_length=50, default='Last Name')