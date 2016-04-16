from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from Reports.models import Report
from Reports.models import MapData
from Reports.models import FormCategory
from forms import DisasterForm
from DisasterReporting.settings import GOOGLE_API_KEY as key
import urllib2
import urllib
import json
import csv

from django.http import StreamingHttpResponse

class Echo(object):
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value

"""Renders the Report Damage form depending on whether the user is logged in"""

def get_form(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
        
    if request.method == 'POST':
        form = DisasterForm(request.POST)
        if form.is_valid():
            try:
                report=make_report(form)
            except:
                return render(request, 'form.html', {'form': form,'address_invalid':True})
            report.save()
            lat=report.latitude
            lng=report.longitude
            return redirect('results',lat,lng)
    else:
        form = DisasterForm()

    return render(request, 'form.html', {'form': form,'address_invalid':False})

def make_report(form):
    lat,lng=get_location(form.cleaned_data['street_address'],form.cleaned_data['city'],form.cleaned_data['state'],form.cleaned_data['zipcode'])
    return Report(first_name=form.cleaned_data['first_name'],
last_name=form.cleaned_data['last_name'],
street_address=form.cleaned_data['street_address'],
city=form.cleaned_data['city'],
state=form.cleaned_data['state'],
zipcode=form.cleaned_data['zipcode'],
type_of_residence=form.cleaned_data['type_of_residence'],
type_of_occupancy=form.cleaned_data['type_of_occupancy'],
type_of_disaster=form.cleaned_data['type_of_disaster'],
date_of_disaster=form.cleaned_data['date_of_disaster'],
insured=form.cleaned_data['insured'],
mortgage=form.cleaned_data['mortgage'],
owned_less_than_30_years=form.cleaned_data['owned_less_than_30_years'],
predisaster_value=form.cleaned_data['predisaster_value'], 

water_damage = form.cleaned_data['water_damage'],

water_mobilehome = form.cleaned_data['water_mobilehome'],

water_mobilehome_minor = form.cleaned_data['water_mobilehome_minor'],

water_mobilehome_major_plywood = form.cleaned_data['water_mobilehome_major_plywood'],
water_mobilehome_major_plywood_yes = form.cleaned_data['water_mobilehome_major_plywood_yes'],
water_mobilehome_major_nonplywood = form.cleaned_data['water_mobilehome_major_nonplywood'],
water_mobilehome_destroyed = form.cleaned_data['water_mobilehome_destroyed'],

water_conventionalhome_minor = form.cleaned_data['water_conventionalhome_minor'],
water_conventionalhome_major = form.cleaned_data['water_conventionalhome_major'],
water_conventionalhome_destroyed = form.cleaned_data['water_conventionalhome_destroyed'],

sewage = form.cleaned_data['sewage'],

minor10_0 = form.cleaned_data['minor10_0'],
minor10_1 = form.cleaned_data['minor10_1'],
minor10_2 = form.cleaned_data['minor10_2'],

major20_0 = form.cleaned_data['major20_0'],
major20_1 = form.cleaned_data['major20_1'],
major20_2 = form.cleaned_data['major20_2'],

major30_0 = form.cleaned_data['major30_0'],
major30_1 = form.cleaned_data['major30_1'],
major30_2 = form.cleaned_data['major30_2'],
major30_3 = form.cleaned_data['major30_3'],

major40_0 = form.cleaned_data['major40_0'],
major40_1 = form.cleaned_data['major40_1'],
major40_2 = form.cleaned_data['major40_2'],

major50_0 = form.cleaned_data['major50_0'],
major50_1 = form.cleaned_data['major50_1'],
major50_2 = form.cleaned_data['major50_2'],

major60_0 = form.cleaned_data['major60_0'],
major60_1 = form.cleaned_data['major60_1'],

major74_0 = form.cleaned_data['major74_0'],
major74_1 = form.cleaned_data['major74_1'],
major74_2 = form.cleaned_data['major74_2'],

destroyed80_0 = form.cleaned_data['destroyed80_0'],
destroyed80_1 = form.cleaned_data['destroyed80_1'],
destroyed80_2 = form.cleaned_data['destroyed80_2'],
destroyed80_3 = form.cleaned_data['destroyed80_3'],
destroyed80_4 = form.cleaned_data['destroyed80_4'],

destroyed90_0 = form.cleaned_data['destroyed90_0'],
destroyed90_1 = form.cleaned_data['destroyed90_1'],

destroyed100_0 = form.cleaned_data['destroyed100_0'],
destroyed100_1 = form.cleaned_data['destroyed100_1'],
latitude=lat,
longitude=lng)

# normal_water=form.cleaned_data['normal_water'],
# normal_destroyed_0=form.cleaned_data['normal_destroyed_0'],
# normal_destroyed_1=form.cleaned_data['normal_destroyed_1'],
# normal_destroyed_2=form.cleaned_data['normal_destroyed_2'],
# normal_destroyed_3=form.cleaned_data['normal_destroyed_3'],
# normal_major_0=form.cleaned_data['normal_major_0'],
# normal_major_1=form.cleaned_data['normal_major_1'],
# normal_major_2=form.cleaned_data['normal_major_2'],
# normal_major_3=form.cleaned_data['normal_major_3'],
# normal_minor_0=form.cleaned_data['normal_minor_0'],
# normal_minor_1=form.cleaned_data['normal_minor_1'],
# normal_minor_2=form.cleaned_data['normal_minor_2'],
# normal_minor_3=form.cleaned_data['normal_minor_3'],
# manufactured_destroyed_0=form.cleaned_data['manufactured_destroyed_0'],
# manufactured_destroyed_1=form.cleaned_data['manufactured_destroyed_1'],
# manufactured_destroyed_2=form.cleaned_data['manufactured_destroyed_2'],
# manufactured_destroyed_3=form.cleaned_data['manufactured_destroyed_3'],
# manufactured_major_0=form.cleaned_data['manufactured_major_0'],
# manufactured_major_1=form.cleaned_data['manufactured_major_1'],
# manufactured_major_2=form.cleaned_data['manufactured_major_2'],
# manufactured_major_3=form.cleaned_data['manufactured_major_3'],
# manufactured_minor_0=form.cleaned_data['manufactured_minor_0'],
# manufactured_minor_1=form.cleaned_data['manufactured_minor_1'],
# manufactured_minor_2=form.cleaned_data['manufactured_minor_2'],
# manufactured_minor_3=form.cleaned_data['manufactured_minor_3'])

def get_locations():
    latlongs=Report.objects.values('id','latitude','longitude')
    labels=[]
    map_labels=[]
    lats=[]
    lngs=[]
    for latlong in latlongs:
        id=latlong['id']
        category=FormCategory.objects.get(pk=id).category_id
        labels.append(category.label)
        map_labels.append(category.map_label)
        lat=latlong['latitude']
        lng=latlong['longitude']
        lats.append(round(lat,3))
        lngs.append(round(lng,3))

    return zip(lats,lngs,map_labels,labels)

def get_location(street_address,city,state,zipcode):
    location=street_address+', '+city+', '+state+' '+str(zipcode)
    query='https://maps.googleapis.com/maps/api/geocode/json?key='+key+'&address='+urllib.quote(location.encode('utf8'),safe='')
    response=urllib2.urlopen(query)
    data=json.load(response)
    lat=data['results'][0]['geometry']['location']['lat']
    lng=data['results'][0]['geometry']['location']['lng']
    return round(lat,10),round(lng,10)

def get_zip_code_damages():
    zip_codes={'minor':[],'major':[],'destroyed':[]}
    minor=0
    major=1
    destroyed=7
    zips = Report.objects.raw('SELECT MIN(R.id) AS id,R.zipcode,MAX(C.map_label) AS damage FROM disaster.reports_report R INNER JOIN disaster.reports_formcategory FC ON R.id=FC.form_id_id INNER JOIN disaster.reports_category C ON FC.category_id_id=C.id GROUP BY zipcode')
    for zip in zips:
        if int(zip.damage)>=destroyed:
             zip_codes['destroyed'].append(zip.zipcode)
        elif int(zip.damage)>=major:
             zip_codes['major'].append(zip.zipcode)
        elif int(zip.damage)>=minor:
             zip_codes['minor'].append(zip.zipcode)
    return zip_codes

def get_zip_code_num_reports():
    zip_codes={'few':[],'several':[],'many':[]}
    few=1
    several=2
    many=4
    zips = Report.objects.raw('SELECT MIN(id) AS id,zipcode,COUNT(*) AS num_reports FROM disaster.reports_report GROUP BY zipcode')
    for zip in zips:
        if zip.num_reports>=many:
             zip_codes['many'].append(zip.zipcode)
        elif zip.num_reports>=several:
             zip_codes['several'].append(zip.zipcode)
        elif zip.num_reports>=few:
             zip_codes['few'].append(zip.zipcode)
    return zip_codes


def show_results(request,lat=None,lng=None):
    map_data=MapData()
    map_data.latitude=lat if lat is not None and lng is not None else 36.2062156
    map_data.longitude=lng if lat is not None and lng is not None else -113.750551
    map_data.zoom=11 if lat is not None and lng is not None else 4
    map_data.locations=get_locations()
    map_data.zip_code_damages=get_zip_code_damages()
    map_data.zip_code_num_reports=get_zip_code_num_reports()
    map_data.api_key=key
    return render(request, 'results.html',{'map_data': map_data})

def get_summaries(request):
    if request.method != 'POST':
        l=list()
        disaster_numbers=[num[0] for num in Report.objects.values_list('fema_disaster_number').distinct()]
        disaster_numbers.insert(0,'All')
        return render(request,'summaries.html',{'disaster_numbers':disaster_numbers})
    num=request.POST['disaster_number']
    if num == 'All':
        data=Report.objects.values_list('zipcode', 'type_of_residence', 'type_of_occupancy', 'type_of_disaster', 'date_of_disaster', 'insured', 'mortgage', 'owned_less_than_30_years', 'predisaster_value', 'water_damage', 'water_mobilehome', 'water_mobilehome_minor', 'water_mobilehome_major_plywood', 'water_mobilehome_major_plywood_yes', 'water_mobilehome_major_nonplywood', 'water_mobilehome_destroyed', 'water_conventionalhome_minor', 'water_conventionalhome_major', 'water_conventionalhome_destroyed', 'sewage', 'minor10_0', 'minor10_1', 'minor10_2', 'major20_0', 'major20_1', 'major20_2', 'major30_0', 'major30_1', 'major30_2', 'major30_3', 'major40_0', 'major40_1', 'major40_2', 'major50_0', 'major50_1', 'major50_2', 'major60_0', 'major60_1', 'major74_0', 'major74_1', 'major74_2', 'destroyed80_0', 'destroyed80_1', 'destroyed80_2', 'destroyed80_3', 'destroyed80_4', 'destroyed90_0', 'destroyed90_1', 'destroyed100_0', 'destroyed100_1', 'perDam', 'estimated_damage', 'fema_disaster_number')
    else:
        data=Report.objects.values_list('zipcode', 'type_of_residence', 'type_of_occupancy', 'type_of_disaster', 'date_of_disaster', 'insured', 'mortgage', 'owned_less_than_30_years', 'predisaster_value', 'water_damage', 'water_mobilehome', 'water_mobilehome_minor', 'water_mobilehome_major_plywood', 'water_mobilehome_major_plywood_yes', 'water_mobilehome_major_nonplywood', 'water_mobilehome_destroyed', 'water_conventionalhome_minor', 'water_conventionalhome_major', 'water_conventionalhome_destroyed', 'sewage', 'minor10_0', 'minor10_1', 'minor10_2', 'major20_0', 'major20_1', 'major20_2', 'major30_0', 'major30_1', 'major30_2', 'major30_3', 'major40_0', 'major40_1', 'major40_2', 'major50_0', 'major50_1', 'major50_2', 'major60_0', 'major60_1', 'major74_0', 'major74_1', 'major74_2', 'destroyed80_0', 'destroyed80_1', 'destroyed80_2', 'destroyed80_3', 'destroyed80_4', 'destroyed90_0', 'destroyed90_1', 'destroyed100_0', 'destroyed100_1', 'perDam', 'estimated_damage', 'fema_disaster_number').filter(fema_disaster_number=num)

    rows = [(idx,)+data[idx] for idx in range(len(data))]
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    rows.insert(0,('id','zipcode', 'type_of_residence', 'type_of_occupancy', 'type_of_disaster', 'date_of_disaster', 'insured', 'mortgage', 'owned_less_than_30_years', 'predisaster_value', 'water_damage', 'water_mobilehome', 'water_mobilehome_minor', 'water_mobilehome_major_plywood', 'water_mobilehome_major_plywood_yes', 'water_mobilehome_major_nonplywood', 'water_mobilehome_destroyed', 'water_conventionalhome_minor', 'water_conventionalhome_major', 'water_conventionalhome_destroyed', 'sewage', 'minor10_0', 'minor10_1', 'minor10_2', 'major20_0', 'major20_1', 'major20_2', 'major30_0', 'major30_1', 'major30_2', 'major30_3', 'major40_0', 'major40_1', 'major40_2', 'major50_0', 'major50_1', 'major50_2', 'major60_0', 'major60_1', 'major74_0', 'major74_1', 'major74_2', 'destroyed80_0', 'destroyed80_1', 'destroyed80_2', 'destroyed80_3', 'destroyed80_4', 'destroyed90_0', 'destroyed90_1', 'destroyed100_0', 'destroyed100_1', 'percent_damaged', 'estimated_damage', 'disaster_number'))
    response = StreamingHttpResponse((writer.writerow(row) for row in rows),
                                     content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="disaster_summary_'+str(num)+'.csv"'
    return response
