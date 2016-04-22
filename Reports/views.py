from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.http import HttpResponseForbidden
from Reports.models import Report
from Reports.models import homevalue
from Reports.models import individual_estimate_model_coefficients
import math
import decimal
import datetime
import random
from Reports.models import MapData
from Reports.models import FormCategory
from Reports.models import Category
from forms import DisasterForm
from DisasterReporting.settings import GOOGLE_API_KEY as key
from DisasterReporting.settings import DISASTER_TIME_CONSTANT
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
                report.username=request.user.username
            except:
                return render(request, 'form.html', {'form': form,'address_invalid':True,'address_duplicate':False})

            if unique_address(report) == 1:
                report.predisaster_value = estimate_home_value(report)
                percent_damage,estimated_damage=calculate_individual_damage_estimate(report)
                report.estimated_damage = estimated_damage
                report.perDam = percent_damage
                report.fema_disaster_number = disaster_number(report)
                report.save()
                category=calculate_category(report)
                category_id=Category.objects.filter(label=category)[0].id
                form_category=FormCategory(form_id_id=report.id,category_id_id=category_id)
                form_category.save()
                return redirect('results',report.id)
            else:
                return render(request, 'form.html', {'form': form,'address_invalid':False,'address_duplicate':True})
    else:
        form = DisasterForm()

    return render(request, 'form.html', {'form': form,'address_invalid':False,'address_duplicate':False})

def unique_address(report):
    inpDate = report.date_of_disaster
    start = inpDate + datetime.timedelta(days=-DISASTER_TIME_CONSTANT)
    end = inpDate + datetime.timedelta(days=DISASTER_TIME_CONSTANT)
    add = Report.objects.filter(date_of_disaster__range = (start,end), street_address = report.street_address, city=report.city, state=report.state, zipcode=report.zipcode)
    if add.exists():
        return 0
    else:
        return 1

def estimate_home_value(report):
    if report.predisaster_value == 0 or report.predisaster_value is None:
        if homevalue.objects.raw('SELECT id, count(zipcode) as c FROM disaster.reports_homevalue WHERE zipcode = %s',[int(report.zipcode)])[0].c >0:
            return homevalue.objects.raw('SELECT id, medhome as c FROM disaster.reports_homevalue WHERE zipcode = %s',[int(report.zipcode)])[0].c
        else:
            ##median home value in US
            return 188900.0
    else:
       return decimal.Decimal(report.predisaster_value)

def calculate_individual_damage_estimate(report):
    coefficients=individual_estimate_model_coefficients.objects.all()
    cur_sum=decimal.Decimal(0.0)
    has_damage=False
    for coefficient in coefficients:
        if should_add_coefficient(coefficient.variable,'owned',report,'type_of_occupancy','Own as primary residence'):
            cur_sum+=coefficient.coefficient
        elif should_add_coefficient(coefficient.variable,'multifamily',report,'type_of_residence','Multi-Family'):
            cur_sum+=coefficient.coefficient
        elif should_add_coefficient(coefficient.variable,'singlefamily',report,'type_of_residence','Single Family'):
            cur_sum+=coefficient.coefficient
        elif should_add_coefficient(coefficient.variable,'earthquake',report,'type_of_disaster','Earthquake'):
            cur_sum+=coefficient.coefficient
        elif should_add_coefficient(coefficient.variable,'fire',report,'type_of_disaster','Fire'):
            cur_sum+=coefficient.coefficient
        elif should_add_coefficient(coefficient.variable,'flood',report,'type_of_disaster','Flooding'):
            cur_sum+=coefficient.coefficient
        elif should_add_coefficient(coefficient.variable,'hurricane',report,'type_of_disaster','Hurricane/Tropical storm'):
            cur_sum+=coefficient.coefficient
        elif should_add_coefficient(coefficient.variable,'mudslide',report,'type_of_disaster','Mud/Landslide'):
            cur_sum+=coefficient.coefficient
        elif should_add_coefficient(coefficient.variable,'other',report,'type_of_disaster','Other'):
            cur_sum+=coefficient.coefficient
        elif should_add_coefficient(coefficient.variable,'tornado',report,'type_of_disaster','Tornado'):
            cur_sum+=coefficient.coefficient
        elif should_add_coefficient(coefficient.variable,'typhoon',report,'type_of_disaster','Typhoon'):
            cur_sum+=coefficient.coefficient
        elif should_add_coefficient(coefficient.variable,'sewage_1',report,'sewage', True):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'minor10_1_1',report,'minor10_1', True):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'minor10_2_1',report,'minor10_2', True):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'major20_0_1',report,'major20_0', True):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'major20_1_1',report,'major20_1', True):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'major20_2_1',report,'major20_2', True):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'major30_0_1',report,'major30_0', True):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'major30_1_1',report,'major30_1', True):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'major30_2_1',report,'major30_2', True):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'major30_3_1',report,'major30_3', True):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'major40_0_1',report,'major40_0', True):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'major40_1_1',report,'major40_1', True):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'major40_2_1',report,'major40_2', True):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'major50_0_1',report,'major50_0', True):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'major50_1_1',report,'major50_1', True):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'major50_2_1',report,'major50_2', True):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'major60_0_1',report,'major60_0', True):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'major60_1_1',report,'major60_1', True):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'major74_0_1',report,'major74_0', True):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'major74_1_1',report,'major74_1', True):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'major74_2_1',report,'major74_2', True):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'destroyed80_0_1',report,'destroyed80_0', True):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'destroyed80_1_1',report,'destroyed80_1', True):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'destroyed80_2_1',report,'destroyed80_2', True):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'destroyed80_3_1',report,'destroyed80_3', True):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'destroyed80_4_1',report,'destroyed80_4', True):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'destroyed90_0_1',report,'destroyed90_0', True):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'destroyed90_1_1',report,'destroyed90_1', True):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'destroyed100_0_1',report,'destroyed100_0', True):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'destroyed100_1_1',report,'destroyed100_1', True):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'water_damage_1',report,'water_damage', True):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'water_mobilehome_1',report,'water_mobilehome', True):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'water_mobilehome_major_plywood_1',report,'water_mobilehome_major_plywood', True):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'water_mobilehome_major_nonplyw_1',report,'water_mobilehome_major_nonplywood', True):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'water_mobilehome_destroyed_1',report,'water_mobilehome_destroyed', True):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'water_conventionalhome_major_1',report,'water_conventionalhome_major', True):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'water_conventionalhome_destroy_1',report,'water_conventionalhome_destroyed', True):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif coefficient.variable == 'predisaster_value':
            cur_sum+=coefficient.coefficient * decimal.Decimal(report.predisaster_value)
        elif coefficient.variable == 'Constant':
            cur_sum+=coefficient.coefficient

    percent_damage = math.exp(cur_sum)/(1+math.exp(cur_sum)) if has_damage else 0
    estimated_damage = decimal.Decimal(percent_damage) * decimal.Decimal(report.predisaster_value)
    if estimated_damage > 31900: #max FEMA grant amount
        estimated_damage = 31900
    return percent_damage,estimated_damage

def should_add_coefficient(variable,var_name,report,report_var_name,report_var_value):
    if variable != var_name:
        return False
    actual_val=getattr(report, report_var_name)
    correct_val = str(actual_val) == str(report_var_value)
    return correct_val

#calculates total disaster cost
def total_disaster_estimate(report):
    if report.type_of_disaster == 'Hurricane/Tropical Storm':
        num = int(disaster_number(report))
        totalEntered = Report.objects.raw('SELECT id, count(*) as c FROM disaster.reports_report WHERE fema_disaster_number = %s',[num])[0].c
        uniqueZip = Report.objects.raw('SELECT id, count(DISTINCT zipcode) as c FROM disaster.reports_report WHERE fema_disaster_number = %s',[num])[0].c
        ####   probability of a new point being in a unique zipcode (based on historical data)
        big = ((1-.01011463)**(uniqueZip-1))*((.01011463)**(totalEntered-uniqueZip-2))
        med = ((1-.08623204)**(uniqueZip-1))*((.08623204)**(totalEntered-uniqueZip-2))
        small = ((1-.06405369)**(uniqueZip-1))*((.06405369)**(totalEntered-uniqueZip-2))
        probBig = big/(big + med + small)
        probMed = med/(big + med +small)

        rand = random.uniform(0,1)
        if rand <= probBig:
            ## based on  damage estimate for hurricanes
            estl = 5425.08*30000
            estu = 5425.08*60000
            return "Estimated total fema payout between %d and %d" % (estl,estu)
        elif rand > probBig and rand <= probBig + probMed:
            ## based on  damage estimate for hurricanes
            estl = 5425.08*10000
            estu = 5425.08*30000
            return "Estimated total fema payout between %d and %d" % (estl,estu)
        else:
            ## based on  damage estimate for hurricanes
            estl = 5425.08*100
            estu = 5425.08*10000
            return "Estimated total fema payout between %d and %d" % (estl,estu)

    elif report.type_of_disaster == "Tornado":
        ## based on  damage estimate for tornados
        estl = 4410.958*380
        estu = 4410.958*1500
        return "Estimated total fema payout between %d and %d" % (estl,estu)

    elif report.type_of_disaster == 'Earthquake':
        ## based on  damage estimate for earthquakes
        estl = 3305.191*3000
        estu = 3305.191*6000
        return "Estimated total fema payout between %d and %d" % (estl,estu)
    else:
        ## based on  damage estimate for floods
        estl = 3564.974*100
        estu = 3564.974*6000
        return "Estimated total fema payout between %d and %d" % (estl,estu)

#sets disaster number
def disaster_number(report):
   inpState = report.state
   inpDisType  = report.type_of_disaster
   inpDate = report.date_of_disaster
   start = inpDate + datetime.timedelta(days=-4)
   end = inpDate + datetime.timedelta(days= 4)
   num = Report.objects.filter(date_of_disaster__range = (start,end), state = inpState, type_of_disaster = inpDisType)
   if not num.exists():
        return Report.objects.raw('SELECT id, max(fema_disaster_number) as a FROM disaster.reports_report')[0].a + 1
   else:
        return Report.objects.filter(date_of_disaster__range = (start,end), state = inpState, type_of_disaster = inpDisType)[0].fema_disaster_number

def calculate_category(report):
    if report.destroyed100_0 == '1' or report.destroyed100_1 == '1':
        return '91-100%'
    if report.destroyed90_0 == '1' or report.destroyed90_1 == '1':
        return '81-90%'
    if report.destroyed80_0 == '1' or report.destroyed80_1 == '1' or report.destroyed80_2 == '1' or report.destroyed80_3 == '1' or report.destroyed80_4 == '1':
        return 'Destroyed (75-80%)'
    if report.water_conventionalhome_destroyed == '1' or report.water_mobilehome_destroyed == '1':
        return 'Destroyed (75-80%)'
    if report.major74_0 == '1' or report.major74_1 == '1' or report.major74_2 == '1':
        return '61-74%'
    if report.major60_0 == '1' or report.major60_1 == '1':
        return '51-60%'
    if report.major50_0 == '1' or report.major50_1 == '1' or report.major50_2 == '1':
        return '41-50%'
    if report.major40_0 == '1' or report.major40_1 == '1' or report.major40_2 == '1':
        return '31-40%'
    if report.major30_0 == '1' or report.major30_1 == '1' or report.major30_2 == '1' or report.major30_3 == '1':
        return '21-30%'
    if report.major20_0 == '1' or report.major20_1 == '1' or report.major20_2 == '1':
        return 'Major (11-20%)'
    if report.water_conventionalhome_major == '1' or report.water_mobilehome_major_nonplywood == '1' or report.water_mobilehome_major_plywood_yes == '1':
        return 'Major (11-20%)'
    if report.minor10_0 == '1' or report.minor10_1 == '1' or report.minor10_2 == '1':
        return 'Minor to 10%'
    if report.water_conventionalhome_minor == '1' or report.water_mobilehome_minor == '1' or report.sewage == '1':
        return 'Minor to 10%'
    return 'None'

def edit_form(request,formid):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    old_report=Report.objects.get(id=formid)
    if old_report.username != request.user.username:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = DisasterForm(request.POST)
        if form.is_valid():
            try:
                report=make_report(form)
                report.username=request.user.username
            except:
                return render(request, 'form.html', {'form': form,'address_invalid':True,'address_duplicate':False})

            report.predisaster_value = estimate_home_value(report)
            percent_damage,estimated_damage=calculate_individual_damage_estimate(report)
            report.estimated_damage = estimated_damage
            report.perDam = percent_damage
            report.fema_disaster_number = disaster_number(report)
            kwargs = update_report(report)
            Report.objects.filter(id=formid).update(**kwargs)
            category = calculate_category(report)
            category_id = Category.objects.filter(label=category)[0].id
            FormCategory.objects.filter(form_id_id=report.id).update(category_id_id=category_id)
            return redirect('results',formid)

    else:
        form=make_form(old_report)
        return render(request, 'form.html', {'form': form,'address_invalid':False,'address_duplicate':False})

def make_form(old_report):
    data=vars(old_report)
    for key,val in data.iteritems():
        if val == 0 and (key != 'predisaster_value' or key != 'estimated_damage' or key != 'perDam'):
            data[key] = False
    return DisasterForm(initial=data)

def update_report(new_report):
    return {'first_name' : new_report.first_name,
'last_name' : new_report.last_name,
'street_address' : new_report.street_address,
'address_line_2' : new_report.address_line_2,
'city' : new_report.city,
'state' : new_report.state,
'zipcode' : new_report.zipcode,
'type_of_residence' : new_report.type_of_residence,
'type_of_occupancy' : new_report.type_of_occupancy,
'type_of_disaster' : new_report.type_of_disaster,
'date_of_disaster' : new_report.date_of_disaster,
'insured' : new_report.insured,
'mortgage' : new_report.mortgage,
'owned_less_than_30_years' : new_report.owned_less_than_30_years,
'predisaster_value' : new_report.predisaster_value,

'water_damage' : new_report.water_damage,

'water_mobilehome' : new_report.water_mobilehome,

'water_mobilehome_minor' : new_report.water_mobilehome_minor,

'water_mobilehome_major_plywood' : new_report.water_mobilehome_major_plywood,
'water_mobilehome_major_plywood_yes' : new_report.water_mobilehome_major_plywood_yes,
'water_mobilehome_major_nonplywood' : new_report.water_mobilehome_major_nonplywood,
'water_mobilehome_destroyed' : new_report.water_mobilehome_destroyed,

'water_conventionalhome_minor' : new_report.water_conventionalhome_minor,
'water_conventionalhome_major' : new_report.water_conventionalhome_major,
'water_conventionalhome_destroyed' : new_report.water_conventionalhome_destroyed,

'sewage' : new_report.sewage,

'minor10_0' : new_report.minor10_0,
'minor10_1' : new_report.minor10_1,
'minor10_2' : new_report.minor10_2,

'major20_0' : new_report.major20_0,
'major20_1' : new_report.major20_1,
'major20_2' : new_report.major20_2,

'major30_0' : new_report.major30_0,
'major30_1' : new_report.major30_1,
'major30_2' : new_report.major30_2,
'major30_3' : new_report.major30_3,

'major40_0' : new_report.major40_0,
'major40_1' : new_report.major40_1,
'major40_2' : new_report.major40_2,

'major50_0' : new_report.major50_0,
'major50_1' : new_report.major50_1,
'major50_2' : new_report.major50_2,

'major60_0' : new_report.major60_0,
'major60_1' : new_report.major60_1,

'major74_0' : new_report.major74_0,
'major74_1' : new_report.major74_1,
'major74_2' : new_report.major74_2,

'destroyed80_0' : new_report.destroyed80_0,
'destroyed80_1' : new_report.destroyed80_1,
'destroyed80_2' : new_report.destroyed80_2,
'destroyed80_3' : new_report.destroyed80_3,
'destroyed80_4' : new_report.destroyed80_4,

'destroyed90_0' : new_report.destroyed90_0,
'destroyed90_1' : new_report.destroyed90_1,

'destroyed100_0' : new_report.destroyed100_0,
'destroyed100_1' : new_report.destroyed100_1,
'latitude' : new_report.latitude,
'longitude' : new_report.longitude,
'estimated_damage':new_report.estimated_damage,
'perDam':new_report.perDam
}

def make_report(form):
    lat,lng=get_location(form.cleaned_data['street_address'],form.cleaned_data['city'],form.cleaned_data['state'],form.cleaned_data['zipcode'])
    return Report(first_name=form.cleaned_data['first_name'],
last_name=form.cleaned_data['last_name'],
street_address=form.cleaned_data['street_address'],
address_line_2=form.cleaned_data['address_line_2'],
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
predisaster_value=form.cleaned_data['predisaster_value'],

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
    map_data.zoom = 6
    map_data.api_key=key
    report = None
    if id is not None:
        report=Report.objects.get(id=id)
        if report is not None:
            map_data.latitude = report.latitude
            map_data.longitude = report.longitude
            map_data.zoom = 11
    if report is None:
        try:
            report=Report.objects.all().last()
        except:
            labels=[]
            map_labels=[]
            lats=[]
            lngs=[]
            map_data.locations=zip(lats,lngs,map_labels,labels)
            map_data.zip_code_damages={'minor':[],'major':[],'destroyed':[]}
            map_data.zip_code_num_reports={'few':[],'several':[],'many':[]}
            return render(request, 'results.html',{'map_data': map_data,'estimate':'0.00','total':'','show_estimate':False})
        map_data.latitude = report.latitude
        map_data.longitude = report.longitude
    show_estimate=False
    if request.user.is_authenticated() and request.user.username == report.username:
        show_estimate=True
    map_data.locations=get_locations(report.fema_disaster_number)
    map_data.zip_code_damages=get_zip_code_damages(report.fema_disaster_number)
    map_data.zip_code_num_reports=get_zip_code_num_reports(report.fema_disaster_number)
    total_estimate = total_disaster_estimate(report)
    return render(request, 'results.html',{'map_data': map_data,'estimate':report.estimated_damage,'total':total_estimate,'show_estimate':show_estimate})

def get_summaries(request):
    state_abbrevs = {
            'AK': 'Alaska',
            'AL': 'Alabama',
            'AR': 'Arkansas',
            'AS': 'American Samoa',
            'AZ': 'Arizona',
            'CA': 'California',
            'CO': 'Colorado',
            'CT': 'Connecticut',
            'DC': 'District of Columbia',
            'DE': 'Delaware',
            'FL': 'Florida',
            'GA': 'Georgia',
            'GU': 'Guam',
            'HI': 'Hawaii',
            'IA': 'Iowa',
            'ID': 'Idaho',
            'IL': 'Illinois',
            'IN': 'Indiana',
            'KS': 'Kansas',
            'KY': 'Kentucky',
            'LA': 'Louisiana',
            'MA': 'Massachusetts',
            'MD': 'Maryland',
            'ME': 'Maine',
            'MI': 'Michigan',
            'MN': 'Minnesota',
            'MO': 'Missouri',
            'MP': 'Northern Mariana Islands',
            'MS': 'Mississippi',
            'MT': 'Montana',
            'NA': 'National',
            'NC': 'North Carolina',
            'ND': 'North Dakota',
            'NE': 'Nebraska',
            'NH': 'New Hampshire',
            'NJ': 'New Jersey',
            'NM': 'New Mexico',
            'NV': 'Nevada',
            'NY': 'New York',
            'OH': 'Ohio',
            'OK': 'Oklahoma',
            'OR': 'Oregon',
            'PA': 'Pennsylvania',
            'PR': 'Puerto Rico',
            'RI': 'Rhode Island',
            'SC': 'South Carolina',
            'SD': 'South Dakota',
            'TN': 'Tennessee',
            'TX': 'Texas',
            'UT': 'Utah',
            'VA': 'Virginia',
            'VI': 'Virgin Islands',
            'VT': 'Vermont',
            'WA': 'Washington',
            'WI': 'Wisconsin',
            'WV': 'West Virginia',
            'WY': 'Wyoming'
    }
    disaster_numbers=[(num.fema_disaster_number,num.type_of_disaster,state_abbrevs[num.state] if len(num.state) == 2 else num.state, num.date_of_disaster, (num.date_of_disaster-datetime.datetime.utcfromtimestamp(0).date()).days) for num in Report.objects.raw('SELECT MIN(ID) as id,fema_disaster_number,type_of_disaster,state,MIN(date_of_disaster) as date_of_disaster FROM disaster.reports_report GROUP BY fema_disaster_number,type_of_disaster,state')]
    disaster_numbers.sort(key=lambda tup: tup[0])
    disaster_numbers.insert(0,('All','All','All','All',0))
    disaster_numbers_by_type={}
    for disaster_number in disaster_numbers:
        if disaster_number[0]=='All':
            continue
        key = disaster_number[1].title() if disaster_number[1] != 'Severe Storm(s)' else 'Severe Storm(s)'
        if not key in disaster_numbers_by_type:
            disaster_numbers_by_type[key] = []
        disaster_numbers_by_type[key].append(disaster_number)
    return render(request,'summaries.html',{'disaster_numbers':disaster_numbers,'disaster_numbers_by_type':disaster_numbers_by_type})

def download_summary(request, id):
    if id == 'All':
        data=Report.objects.values_list('zipcode', 'type_of_residence', 'type_of_occupancy', 'type_of_disaster', 'date_of_disaster', 'insured', 'mortgage', 'owned_less_than_30_years', 'predisaster_value', 'water_damage', 'water_mobilehome', 'water_mobilehome_minor', 'water_mobilehome_major_plywood', 'water_mobilehome_major_plywood_yes', 'water_mobilehome_major_nonplywood', 'water_mobilehome_destroyed', 'water_conventionalhome_minor', 'water_conventionalhome_major', 'water_conventionalhome_destroyed', 'sewage', 'minor10_0', 'minor10_1', 'minor10_2', 'major20_0', 'major20_1', 'major20_2', 'major30_0', 'major30_1', 'major30_2', 'major30_3', 'major40_0', 'major40_1', 'major40_2', 'major50_0', 'major50_1', 'major50_2', 'major60_0', 'major60_1', 'major74_0', 'major74_1', 'major74_2', 'destroyed80_0', 'destroyed80_1', 'destroyed80_2', 'destroyed80_3', 'destroyed80_4', 'destroyed90_0', 'destroyed90_1', 'destroyed100_0', 'destroyed100_1', 'perDam', 'estimated_damage', 'fema_disaster_number')
    else:
        data=Report.objects.values_list('zipcode', 'type_of_residence', 'type_of_occupancy', 'type_of_disaster', 'date_of_disaster', 'insured', 'mortgage', 'owned_less_than_30_years', 'predisaster_value', 'water_damage', 'water_mobilehome', 'water_mobilehome_minor', 'water_mobilehome_major_plywood', 'water_mobilehome_major_plywood_yes', 'water_mobilehome_major_nonplywood', 'water_mobilehome_destroyed', 'water_conventionalhome_minor', 'water_conventionalhome_major', 'water_conventionalhome_destroyed', 'sewage', 'minor10_0', 'minor10_1', 'minor10_2', 'major20_0', 'major20_1', 'major20_2', 'major30_0', 'major30_1', 'major30_2', 'major30_3', 'major40_0', 'major40_1', 'major40_2', 'major50_0', 'major50_1', 'major50_2', 'major60_0', 'major60_1', 'major74_0', 'major74_1', 'major74_2', 'destroyed80_0', 'destroyed80_1', 'destroyed80_2', 'destroyed80_3', 'destroyed80_4', 'destroyed90_0', 'destroyed90_1', 'destroyed100_0', 'destroyed100_1', 'perDam', 'estimated_damage', 'fema_disaster_number').filter(fema_disaster_number=id)

    rows = [(idx,)+data[idx] for idx in range(len(data))]
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    rows.insert(0,('id','zipcode', 'type_of_residence', 'type_of_occupancy', 'type_of_disaster', 'date_of_disaster', 'insured', 'mortgage', 'owned_less_than_30_years', 'predisaster_value', 'water_damage', 'water_mobilehome', 'water_mobilehome_minor', 'water_mobilehome_major_plywood', 'water_mobilehome_major_plywood_yes', 'water_mobilehome_major_nonplywood', 'water_mobilehome_destroyed', 'water_conventionalhome_minor', 'water_conventionalhome_major', 'water_conventionalhome_destroyed', 'sewage', 'minor10_0', 'minor10_1', 'minor10_2', 'major20_0', 'major20_1', 'major20_2', 'major30_0', 'major30_1', 'major30_2', 'major30_3', 'major40_0', 'major40_1', 'major40_2', 'major50_0', 'major50_1', 'major50_2', 'major60_0', 'major60_1', 'major74_0', 'major74_1', 'major74_2', 'destroyed80_0', 'destroyed80_1', 'destroyed80_2', 'destroyed80_3', 'destroyed80_4', 'destroyed90_0', 'destroyed90_1', 'destroyed100_0', 'destroyed100_1', 'percent_damaged', 'estimated_damage', 'disaster_number'))
    response = StreamingHttpResponse((writer.writerow(row) for row in rows),
                                     content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="disaster_summary_'+str(id)+'.csv"'
    return response