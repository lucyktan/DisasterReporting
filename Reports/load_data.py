import django
from django.conf import settings
from DisasterReporting import settings as sett
settings.configure(default_settings=sett, DEBUG=True)
django.setup()

#print(settings.INSTALLED_APPS)

# Full path and name to your csv file
csv_filepathname = "C:/Users/Katie Pezzot/Desktop/disaster/Reports/zillow.csv"
# Full path to your django project directory
your_djangoproject_home = "C:/Users/Katie Pezzot/Desktop/disaster/"

#import sys,os
#sys.path.append(your_djangoproject_home)
#os.environ['DJANGO_SETTINGS_MODULE'] = 'DisasterReporting.settings'

from models import homevalue

import csv
dataReader = csv.reader(open(csv_filepathname), delimiter=',', quotechar='"')

for row in dataReader:
    if row[0] != 'zipcode': # Ignore the header row, import everything else
        home = homevalue()
        home.zipcode = row[0]
        home.medhome = row[1]
        home.sqfthome = row[2]
        home.rent = row[3]
        home.save()
