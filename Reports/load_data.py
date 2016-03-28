import os
import csv

import django
import sys
sys.path.insert(0,'..')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DisasterReporting.settings")
django.setup()

from Reports.models import homevalue
from Reports.models import disaster_history
from Reports.models import owners
from Reports.models import renters
from Reports.models import Category

def import_disaster_history():
    disaster_history.objects.all().delete()
    csv_filepathname = os.getcwd()+'/DisasterDeclarationsSummaries.csv'
    dataReader = csv.reader(open(csv_filepathname), delimiter=',', quotechar='"')
    for row in dataReader:
        if row[0]!='dishist_id': # Ignore the header row, import everything else
            disaster = disaster_history()
            disaster.dishist_id = row[0]
            disaster.disasterNumber = row[1]
            disaster.ihProgramDeclared = row[2]
            disaster.iaProgramDeclared = row[3]
            disaster.paProgramDeclared = row[4]
            disaster.hmProgramDeclared = row[5]
            disaster.state = row[6]
            disaster.disasterType = row[7]
            disaster.incidentType = row[8]
            disaster.year = row[9]
            disaster.save()

def import_owners():
    owners.objects.all().delete()
    csv_filepathname = os.getcwd()+'/HousingAssistanceOwners.csv'
    dataReader = csv.reader(open(csv_filepathname), delimiter=',', quotechar='"')
    for row in dataReader:
        if row[0]!='dishist_id': # Ignore the header row, import everything else
            disaster = owners()
            disaster.owners_id = row[0]
            disaster.disasterNumber = row[1]
            disaster.state = row[2]
            disaster.county = row[3]
            disaster.zipCode = row[4] if row[4].isdigit() else None
            disaster.averageFemaInspectedDamage = row[5]
            disaster.totalDamage = row[6]
            disaster.noFemaInspectedDamage = row[7]
            disaster.FemaInspectedDamageBetween1And10000 = row[8]
            disaster.FemaInspectedDamageBetween10001And20000 = row[9]
            disaster.FemaInspectedDamageBetweens20001And30000 = row[10]
            disaster.FemaInspectedDamageGreaterThan30000 = row[11]
            disaster.ApprovedForFemaAssistance = row[12]
            disaster.RepairReplaceAmount = row[13]
            disaster.RentalAmount = row[14]
            disaster.OtherNeedsAmount = row[15]
            disaster.ApprovedBetween1And10000 = row[16]
            disaster.ApprovedBetween100001And25000 = row[17]
            disaster.ApprovedBetween25001AndMax = row[18]
            disaster.TotalMaxGrants = row[19]
            disaster.save()

def import_renters():
    renters.objects.all().delete()
    csv_filepathname = os.getcwd()+'/HousingAssistanceRenters.csv'
    dataReader = csv.reader(open(csv_filepathname), delimiter=',', quotechar='"')
    for row in dataReader:
        if row[0]!='renters_id': # Ignore the header row, import everything else
            disaster = renters()
            disaster.renters_id = row[0]
            disaster.disasterNumber = row[1]
            disaster.state = row[2]
            disaster.county = row[3]
            disaster.zipCode = row[4] if row[4].isdigit() else None
            disaster.validRegistrations = row[5]
            disaster.TotalInspectedWithNoDamage = row[6]
            disaster.TotalWithModerateDamage = row[7]
            disaster.TotalWithMajorDamage = row[8]
            disaster.TotalWithSubstantialDamage = row[9]
            disaster.ApprovedForFemaAssistance = row[10]
            disaster.RepairReplaceAmount = row[11]
            disaster.RentalAmount = row[12]
            disaster.OtherNeedsAmount = row[13]
            disaster.ApprovedBetween1And10000 = row[14]
            disaster.ApprovedBetween10001And25000 = row[15]
            disaster.ApprovedBetween25001AndMax = row[16]
            disaster.TotalMaxGrants = row[17]
            disaster.save()

def import_homevalue():
    homevalue.objects.all().delete()
    csv_filepathname = os.getcwd()+'/zillow.csv'
    dataReader = csv.reader(open(csv_filepathname), delimiter=',', quotechar='"')
    for row in dataReader:
        if row[0] != 'zipcode': # Ignore the header row, import everything else
            home = homevalue()
            home.zipcode = row[0]
            home.medhome = row[1]
            home.sqfthome = row[2]
            home.rent = row[3]
            home.save()

def import_categories():
    Category.objects.all().delete()
    csv_filepathname = os.getcwd()+'/categories.csv'
    dataReader = csv.reader(open(csv_filepathname), delimiter=',', quotechar='"')
    for row in dataReader:
        category = Category()
        category.map_label = row[0]
        category.label = row[1]
        category.save()

import_homevalue()
import_disaster_history()
import_owners()
import_renters()
import_categories()