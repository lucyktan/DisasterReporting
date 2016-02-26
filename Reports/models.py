from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Report(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    type_of_residence = models.CharField(max_length=50)
    type_of_occupancy = models.CharField(max_length=50)
    type_of_disaster = models.CharField(max_length=50)
    date_of_disaster = models.DateField(auto_now=False, auto_now_add=False)
    insured = models.IntegerField()
    mortgage = models.IntegerField()
    owned_less_than_30_years=models.IntegerField()
    predisaster_value = models.DecimalField(max_digits=50, decimal_places=2)

    normal_water = models.CharField(max_length=50)

    normal_destroyed_0 = models.IntegerField()
    normal_destroyed_1 = models.IntegerField()
    normal_destroyed_2 = models.IntegerField()
    normal_destroyed_3 = models.IntegerField()

    normal_major_0 = models.IntegerField()
    normal_major_1 = models.IntegerField()
    normal_major_2 = models.IntegerField()
    normal_major_3 = models.IntegerField()

    normal_minor_0 = models.IntegerField()
    normal_minor_1 = models.IntegerField()
    normal_minor_2 = models.IntegerField()
    normal_minor_3 = models.IntegerField()

    manufactured_destroyed_0 = models.IntegerField()
    manufactured_destroyed_1 = models.IntegerField()
    manufactured_destroyed_2 = models.IntegerField()
    manufactured_destroyed_3 = models.IntegerField()

    manufactured_major_0 = models.IntegerField()
    manufactured_major_1 = models.IntegerField()
    manufactured_major_2 = models.IntegerField()
    manufactured_major_3 = models.IntegerField()

    manufactured_minor_0 = models.IntegerField()
    manufactured_minor_1 = models.IntegerField()
    manufactured_minor_2 = models.IntegerField()
    manufactured_minor_3 = models.IntegerField()
