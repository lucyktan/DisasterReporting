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
from Reports.models import Report

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

def import_report_owner():
    Report.objects.all().delete()
    csv_filepathname = os.getcwd()+'/dbMergeOwn.csv'
    dataReader = csv.reader(open(csv_filepathname), delimiter=',', quotechar='"')
    for row in dataReader:
        if row[0]!='street_address': # Ignore the header row, import everything else
            disaster = Report()
            disaster.street_address = row[0]
            disaster.city = row[1]
            disaster.state = row[2]
            disaster.zipcode = row[3]
            disaster.predisaster_value = row[4]
            disaster.type_of_residence = row[5]
            disaster.type_of_occupancy = row[6]
            disaster.type_of_disaster = row[7]
            disaster.insured = row[8]
            disaster.sewage = row[9]
            disaster.minor10_0 = row[10]
            disaster.minor10_1 = row[11]
            disaster.minor10_2 = row[12]
            disaster.major20_0 = row[13]
            disaster.major20_1 = row[14]
            disaster.major20_2 = row[15]
            disaster.major30_0 = row[16]
            disaster.major30_1 = row[17]
            disaster.major30_2 = row[18]
            disaster.major30_3 = row[19]
            disaster.major40_0 = row[20]
            disaster.major40_1 = row[21]
            disaster.major40_2 = row[22]
            disaster.major50_0 = row[23]
            disaster.major50_1 = row[24]
            disaster.major50_2 = row[25]
            disaster.major60_0 = row[26]
            disaster.major60_1 = row[27]
            disaster.major74_0 = row[28]
            disaster.major74_1 = row[29]
            disaster.major74_2 = row[30]
            disaster.destroyed80_0 = row[31]
            disaster.destroyed80_1 = row[32]
            disaster.destroyed80_2 = row[33]
            disaster.destroyed80_3 = row[34]
            disaster.destroyed80_4 = row[35]
            disaster.destroyed90_0 = row[36]
            disaster.destroyed90_1 = row[37]
            disaster.destroyed100_0 = row[38]
            disaster.destroyed100_1 = row[39]
            disaster.perDam = row[40]
            disaster.estimated_damage = row[41]
            disaster.fema_disaster_number = row[42]
            disaster.first_name = row[43]
            disaster.last_name = row[44]
            disaster.date_of_disaster = row[45]
            disaster.mortgage = row[46]
            disaster.owned_less_than_30_years = row[47]
            disaster.water_damage = row[48]
            disaster.water_mobilehome = row[49]
            disaster.water_mobilehome_minor = row[50]
            disaster.water_mobilehome_major_plywood = row[51]
            disaster.water_mobilehome_major_plywood_yes = row[52]
            disaster.water_mobilehome_major_nonplywood = row[53]
            disaster.water_mobilehome_destroyed = row[54]
            disaster.water_conventionalhome_minor = row[55]
            disaster.water_conventionalhome_major = row[56]
            disaster.water_conventionalhome_destroyed = row[57]
            disaster.save()

def import_report_renter():
    csv_filepathname = os.getcwd()+'/dbMergeRen.csv'
    dataReader = csv.reader(open(csv_filepathname), delimiter=',', quotechar='"')
    for row in dataReader:
        if row[0]!='street_address': # Ignore the header row, import everything else
            disaster = Report()
            disaster.street_address = row[0]
            disaster.city = row[1]
            disaster.state = row[2]
            disaster.zipcode = row[3]
            disaster.predisaster_value = row[4]
            disaster.type_of_residence = row[5]
            disaster.type_of_occupancy = row[6]
            disaster.type_of_disaster = row[7]
            disaster.insured = row[8]
            disaster.sewage = row[9]
            disaster.minor10_0 = row[10]
            disaster.minor10_1 = row[11]
            disaster.minor10_2 = row[12]
            disaster.major20_0 = row[13]
            disaster.major20_1 = row[14]
            disaster.major20_2 = row[15]
            disaster.major30_0 = row[16]
            disaster.major30_1 = row[17]
            disaster.major30_2 = row[18]
            disaster.major30_3 = row[19]
            disaster.major40_0 = row[20]
            disaster.major40_1 = row[21]
            disaster.major40_2 = row[22]
            disaster.major50_0 = row[23]
            disaster.major50_1 = row[24]
            disaster.major50_2 = row[25]
            disaster.major60_0 = row[26]
            disaster.major60_1 = row[27]
            disaster.major74_0 = row[28]
            disaster.major74_1 = row[29]
            disaster.major74_2 = row[30]
            disaster.destroyed80_0 = row[31]
            disaster.destroyed80_1 = row[32]
            disaster.destroyed80_2 = row[33]
            disaster.destroyed80_3 = row[34]
            disaster.destroyed80_4 = row[35]
            disaster.destroyed90_0 = row[36]
            disaster.destroyed90_1 = row[37]
            disaster.destroyed100_0 = row[38]
            disaster.destroyed100_1 = row[39]
            disaster.perDam = row[40]
            disaster.estimated_damage = row[41]
            disaster.fema_disaster_number = row[42]
            disaster.first_name = row[43]
            disaster.last_name = row[44]
            disaster.date_of_disaster = row[45]
            disaster.mortgage = row[46]
            disaster.owned_less_than_30_years = row[47]
            disaster.water_damage = row[48]
            disaster.water_mobilehome = row[49]
            disaster.water_mobilehome_minor = row[50]
            disaster.water_mobilehome_major_plywood = row[51]
            disaster.water_mobilehome_major_plywood_yes = row[52]
            disaster.water_mobilehome_major_nonplywood = row[53]
            disaster.water_mobilehome_destroyed = row[54]
            disaster.water_conventionalhome_minor = row[55]
            disaster.water_conventionalhome_major = row[56]
            disaster.water_conventionalhome_destroyed = row[57]
            disaster.save()

import_homevalue()
import_disaster_history()
import_owners()
import_renters()
import_report_owner()
import_report_renter()