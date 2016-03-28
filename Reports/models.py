from __future__ import unicode_literals

from django.db import models

#Create your models here.
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

class homevalue(models.Model):
    class Meta:
        app_label = 'Reports'
    zipcode = models.IntegerField()
    medhome = models.IntegerField()
    sqfthome = models.IntegerField()
    rent = models.IntegerField()
    def __str__(self):
        return homevalue.content
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

    latitude=models.DecimalField(max_digits=15,decimal_places=10)
    longitude=models.DecimalField(max_digits=15,decimal_places=10)

class MapData():
    locations=[]
    latitude=0
    longitude=0
    api_key=''
    zoom=4

class Category(models.Model):
    map_label=models.CharField(max_length=1)
    label=models.CharField(max_length=50)

class FormCategory(models.Model):
    form_id=models.OneToOneField(Report,on_delete=models.CASCADE,
        primary_key=True)
    category_id=models.ForeignKey(Category,on_delete=models.SET_NULL,null=True)