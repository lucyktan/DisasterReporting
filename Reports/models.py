from __future__ import unicode_literals
from django.db import models
import datetime

"""Historical data from FEMA's PDA documents"""
class disaster_history(models.Model):
    dishist_id = models.IntegerField()
    disasterNumber = models.IntegerField()
    ihProgramDeclared = models.IntegerField()
    iaProgramDeclared = models.IntegerField()
    paProgramDeclared = models.IntegerField()
    hmProgramDeclared = models.IntegerField()
    state = models.CharField(max_length=2)
    disasterType = models.CharField(max_length=2)
    incidentType = models.CharField(max_length=16)
    year = models.IntegerField()

"""Property values data from Zillow"""
class homevalue(models.Model):
    class Meta:
        app_label = 'Reports'
    zipcode = models.IntegerField()
    medhome = models.IntegerField()
    sqfthome = models.IntegerField()
    rent = models.IntegerField()
    def __str__(self):
        return homevalue.content

"""Historical disaster data from property owners provided by FEMA"""       
class owners(models.Model):
    owners_id = models.IntegerField()
    disasterNumber = models.IntegerField()
    state = models.CharField(max_length=2)
    county = models.CharField(max_length=26)
    zipCode = models.IntegerField(null=True)
    averageFemaInspectedDamage = models.IntegerField()
    totalDamage = models.IntegerField()
    noFemaInspectedDamage = models.IntegerField()
    FemaInspectedDamageBetween1And10000 = models.IntegerField()
    FemaInspectedDamageBetween10001And20000 = models.IntegerField()
    FemaInspectedDamageBetweens20001And30000 = models.IntegerField()
    FemaInspectedDamageGreaterThan30000 = models.IntegerField()
    ApprovedForFemaAssistance = models.IntegerField()
    RepairReplaceAmount = models.DecimalField(decimal_places=2,max_digits=30)
    RentalAmount = models.DecimalField(decimal_places=2,max_digits=30)
    OtherNeedsAmount = models.DecimalField(decimal_places=2,max_digits=30)
    ApprovedBetween1And10000 = models.IntegerField()
    ApprovedBetween100001And25000 = models.IntegerField()
    ApprovedBetween25001AndMax = models.IntegerField()
    TotalMaxGrants = models.IntegerField()

"""Historical disaster data from property renters provided by FEMA"""
class renters(models.Model):
    renters_id = models.IntegerField()
    disasterNumber = models.IntegerField()
    state = models.CharField(max_length=2)
    county = models.CharField(max_length=26)
    zipCode = models.IntegerField(null=True)
    validRegistrations = models.IntegerField()
    TotalInspectedWithNoDamage = models.IntegerField()
    TotalWithModerateDamage = models.IntegerField()
    TotalWithMajorDamage = models.IntegerField()
    TotalWithSubstantialDamage = models.IntegerField()
    ApprovedForFemaAssistance = models.IntegerField()
    RepairReplaceAmount = models.DecimalField(decimal_places=2,max_digits=30)
    RentalAmount = models.DecimalField(decimal_places=2,max_digits=30)
    OtherNeedsAmount = models.DecimalField(decimal_places=2,max_digits=30)
    ApprovedBetween1And10000 = models.IntegerField()
    ApprovedBetween10001And25000 = models.IntegerField()
    ApprovedBetween25001AndMax = models.IntegerField()
    TotalMaxGrants = models.IntegerField()

"""Submitted information from the Report Damage form"""
class Report(models.Model):
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')
    street_address = models.CharField(max_length=100, default='')
    city = models.CharField(max_length=100, default='')
    state = models.CharField(max_length=50, default='')
    zipcode = models.IntegerField(default=0)
    type_of_residence = models.CharField(max_length=50, default='')
    type_of_occupancy = models.CharField(max_length=50, default='')
    type_of_disaster = models.CharField(max_length=50, default='')
    date_of_disaster = models.DateField(auto_now=False, auto_now_add=False, default=datetime.date.today())

    insured = models.IntegerField(default=0)
    mortgage = models.IntegerField(default=0)
    owned_less_than_30_years=models.IntegerField(default=0)
    predisaster_value = models.DecimalField(max_digits=50, decimal_places=2, default=0)

    water_damage = models.IntegerField(default=0)

    water_mobilehome = models.IntegerField(default=0)

    water_mobilehome_minor = models.IntegerField(default=0)

    water_mobilehome_major_plywood = models.IntegerField(default=0)
    water_mobilehome_major_plywood_yes = models.IntegerField(default=0)
    water_mobilehome_major_nonplywood = models.IntegerField(default=0)
    water_mobilehome_destroyed = models.IntegerField(default=0)

    water_conventionalhome_minor = models.IntegerField(default=0)
    water_conventionalhome_major = models.IntegerField(default=0)
    water_conventionalhome_destroyed = models.IntegerField(default=0)

    sewage = models.IntegerField(default=0)

    minor10_0 = models.IntegerField(default=0)
    minor10_1 = models.IntegerField(default=0)
    minor10_2 = models.IntegerField(default=0)

    major20_0 = models.IntegerField(default=0)
    major20_1 = models.IntegerField(default=0)
    major20_2 = models.IntegerField(default=0)

    major30_0 = models.IntegerField(default=0)
    major30_1 = models.IntegerField(default=0)
    major30_2 = models.IntegerField(default=0)
    major30_3 = models.IntegerField(default=0)

    major40_0 = models.IntegerField(default=0)
    major40_1 = models.IntegerField(default=0)
    major40_2 = models.IntegerField(default=0)

    major50_0 = models.IntegerField(default=0)
    major50_1 = models.IntegerField(default=0)
    major50_2 = models.IntegerField(default=0)

    major60_0 = models.IntegerField(default=0)
    major60_1 = models.IntegerField(default=0)

    major74_0 = models.IntegerField(default=0)
    major74_1 = models.IntegerField(default=0)
    major74_2 = models.IntegerField(default=0)

    destroyed80_0 = models.IntegerField(default=0)
    destroyed80_1 = models.IntegerField(default=0)
    destroyed80_2 = models.IntegerField(default=0)
    destroyed80_3 = models.IntegerField(default=0)
    destroyed80_4 = models.IntegerField(default=0)

    destroyed90_0 = models.IntegerField(default=0)
    destroyed90_1 = models.IntegerField(default=0)

    destroyed100_0 = models.IntegerField(default=0)
    destroyed100_1 = models.IntegerField(default=0)

    perDam= models.DecimalField(max_digits=20,decimal_places=4, default=-1.0000)
    estimated_damage= models.DecimalField(max_digits=20,decimal_places=2, default=-1.00)
    fema_disaster_number = models.IntegerField(default=-1)

class individual_estimate_model_coefficients(models.Model):
    variable=models.CharField(max_length=50)
    coefficient=models.DecimalField(max_digits=20,decimal_places=8)