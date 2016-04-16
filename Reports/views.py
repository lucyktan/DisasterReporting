from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from Reports.models import Report
from Reports.models import MapData
from Reports.models import FormCategory
from Reports.models import Category
from forms import DisasterForm
from DisasterReporting.settings import GOOGLE_API_KEY as key
import urllib2
import urllib
import json

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
            category=calculate_category(report)
            category_id=Category.objects.filter(label=category)[0].id
            form_category=FormCategory(form_id_id=report.id,category_id_id=category_id)
            form_category.save()
            return redirect('results',report.id)
    else:
        form = DisasterForm()

    return render(request, 'form.html', {'form': form,'address_invalid':False})

def calculate_category(report):
    if report.destroyed100_0 == 1 or report.destroyed100_1 == 1:
        return '91-100%'
    if report.destroyed90_0 == 1 or report.destroyed90_1 == 1:
        return '81-90%'
    if report.destroyed80_0 == 1 or report.destroyed80_1 == 1 or report.destroyed80_2 == 1 or report.destroyed80_3 == 1 or report.destroyed80_4 == 1:
        return 'Destroyed (75-80%)'
    if report.water_conventionalhome_destroyed == 1 or report.water_mobilehome_destroyed == 1:
        return 'Destroyed (75-80%)'
    if report.major74_0 == 1 or report.major74_1 == 1 or report.major74_2 == 1:
        return '61-74%'
    if report.major60_0 == 1 or report.major60_1 == 1:
        return '51-60%'
    if report.major50_0 == 1 or report.major50_1 == 1 or report.major50_2 == 1:
        return '41-50%'
    if report.major40_0 == 1 or report.major40_1 == 1 or report.major40_2 == 1:
        return '31-40%'
    if report.major30_0 == 1 or report.major30_1 == 1 or report.major30_2 == 1 or report.major30_3 == 1:
        return '21-30%'
    if report.major20_0 == 1 or report.major20_1 == 1 or report.major20_2 == 1:
        return 'Major (11-20%)'
    if report.water_conventionalhome_major == 1 or report.water_mobilehome_major_nonplywood == 1 or report.water_mobilehome_major_plywood_yes == 1:
        return 'Major (11-20%)'
    if report.minor10_0 == 1 or report.minor10_1 == 1 or report.minor10_2 == 1:
        return 'Minor to 10%'
    if report.water_conventionalhome_minor == 1 or report.water_mobilehome_minor == 1 or report.sewage == 1:
        return 'Minor to 10%'
    return 'None'

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

def get_locations(disaster_num):
    latlongs=Report.objects.filter(fema_disaster_number=disaster_num).values('id','latitude','longitude')
    labels=[]
    map_labels=[]
    lats=[]
    lngs=[]
    for latlong in latlongs:
        id=latlong['id']
        try:
            category=FormCategory.objects.get(pk=id).category_id
            labels.append(category.label)
            map_labels.append(category.map_label)
            lat=latlong['latitude']
            lng=latlong['longitude']
            lats.append(round(lat,3))
            lngs.append(round(lng,3))
        except:
            pass

    return zip(lats,lngs,map_labels,labels)

def get_location(street_address,city,state,zipcode):
    location=street_address+', '+city+', '+state+' '+str(zipcode)
    query='https://maps.googleapis.com/maps/api/geocode/json?key='+key+'&address='+urllib.quote(location.encode('utf8'),safe='')
    response=urllib2.urlopen(query)
    data=json.load(response)
    lat=data['results'][0]['geometry']['location']['lat']
    lng=data['results'][0]['geometry']['location']['lng']
    return round(lat,10),round(lng,10)

def get_zip_code_damages(disaster_num):
    zip_codes={'minor':[],'major':[],'destroyed':[]}
    minor=0
    major=1
    destroyed=7
    zips = Report.objects.raw('SELECT MIN(R.id) AS id,R.zipcode,MAX(C.map_label) AS damage FROM disaster.reports_report R INNER JOIN disaster.reports_formcategory FC ON R.fema_disaster_number = ' + str(disaster_num) + ' AND R.id=FC.form_id_id INNER JOIN disaster.reports_category C ON FC.category_id_id=C.id WHERE C.label<>\'None\' GROUP BY zipcode')
    for zip in zips:
        if int(zip.damage)>=destroyed:
             zip_codes['destroyed'].append(zip.zipcode)
        elif int(zip.damage)>=major:
             zip_codes['major'].append(zip.zipcode)
        elif int(zip.damage)>=minor:
             zip_codes['minor'].append(zip.zipcode)
    return zip_codes

def get_zip_code_num_reports(disaster_num):
    zip_codes={'few':[],'several':[],'many':[]}
    few=1
    several=2
    many=4
    zips = Report.objects.raw('SELECT MIN(id) AS id,zipcode,COUNT(*) AS num_reports FROM disaster.reports_report WHERE fema_disaster_number = ' + str(disaster_num) + ' GROUP BY zipcode')
    for zip in zips:
        if zip.num_reports>=many:
             zip_codes['many'].append(zip.zipcode)
        elif zip.num_reports>=several:
             zip_codes['several'].append(zip.zipcode)
        elif zip.num_reports>=few:
             zip_codes['few'].append(zip.zipcode)
    return zip_codes


def show_results(request,id=None):
    map_data=MapData()
    map_data.latitude = 36.2062156
    map_data.longitude = -113.750551
    map_data.zoom = 4
    report = None
    if id is not None:
        report=Report.objects.get(id=id)
        if report is not None:
            map_data.latitude = report.latitude
            map_data.longitude = report.longitude
            map_data.zoom = 11
    if report is None:
        report=Report.objects.all().last()

    map_data.locations=get_locations(report.fema_disaster_number)
    map_data.zip_code_damages=get_zip_code_damages(report.fema_disaster_number)
    map_data.zip_code_num_reports=get_zip_code_num_reports(report.fema_disaster_number)
    map_data.api_key=key
    return render(request, 'results.html',{'map_data': map_data})