from __future__ import unicode_literals

from django.db import models

# Create your models here.
#class disaster_history(models.Model):
#    dishist_id = models.IntegerField()
#    disasterNumber = models.IntegerField()
#    ihProgramDeclared = models.IntegerField()
#    iaProgramDeclared = models.IntegerField()
#    paProgramDeclared = models.IntegerField()
#    hmProgramDeclared = models.IntegerField()
#    state = models.CharField(max_length=2)
 #   disasterType = models.CharField(max_length=2)
 #   incidentType = models.CharField(max_length=15)
  #  year = models.IntegerField()

class homevalue(models.Model):
    zipcode = models.IntegerField()
    medhome = models.IntegerField()
    sqfthome = models.IntegerField()
    rent = models.IntegerField()
    def __str__(self):
        return homevalue.content
#class owners(models.Model):
#    owners_id = models.IntegerField()
#    disasterNumber = models.IntegerField()
#    state = models.CharField(max_length=2)
#    county = models.charField(max_length=26)
#    zipCode = models.IntegerField()
#    averageFemaInspectedDamage = models.IntegerField()
#    totalDamage = models.IntegerField()
#    noFemaInspectedDamage = models.IntegerField()
#    FemaInspectedDamageBetween1And10000 = models.IntegerField()
#    FemaInspectedDamageBetween10001And20000 = models.IntegerField()
#    FemaInspectedDamageBetweens20001And30000 = models.IntegerField()
#    FemaInspectedDamageGreaterThan30000 = models.IntegerField()
#    ApprovedForFemaAssistance = models.IntegerField()
#    RepairReplaceAmount = models.IntegerField()
#    RentalAmount = models.IntegerField()
'''    OtherNeedsAmount = models.IntegerField()
    ApprovedBetween1And10000 = models.IntegerField()
    ApprovedBetween100001And25000 = models.IntegerField()
    ApprovedBetween25001AndMax = models.IntegerField()
    TotalMaxGrants = models.IntegerField()

class renters(models.Model):
    renters_id = models.IntegerField()
    disasterNumber = models.IntegerField()
    state = models.CharField(max_length=2)
    county = models.charField(max_length=26)
    zipCode = models.IntegerField()
    validRegistrations = models.IntegerField()
    TotalInspectedWithNoDamage = models.IntegerField()
    TotalWithModerateDamage = models.IntegerField()
    TotalWithMajorDamage = models.IntegerField()
    TotalWithSubstantialDamage = models.IntegerField()
    ApprovedForFemaAssistance = models.IntegerField()
    RepairReplaceAmount = models.IntegerField()
    RentalAmount = models.IntegerField()
    OtherNeedsAmount = models.IntegerField()
    ApprovedBetween1And10000 = models.IntegerField()
    ApprovedBetween10001And25000 = models.IntegerField()
    ApprovedBetween25001AndMax = models.IntegerField()
    TotalMaxGrants = models.IntegerField()'''