from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from Reports.models import Report
from Reports.models import individual_estimate_model_coefficients
from forms import DisasterForm
import math
import decimal
import datetime
import random

"""Renders the Report Damage form depending on whether the user is logged in"""

def get_form(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
        
    if request.method == 'POST':
        form = DisasterForm(request.POST)
        if form.is_valid():
            report=make_report(form)
            percent_damage,estimated_damage=calculate_individual_damage_estimate(report)
            report.estimated_damage = estimated_damage
            report.perDam = percent_damage
            report.fema_disaster_number = disaster_number(report)
            total_estimate = total_disaster_estimate(report)
            report.save()
            return redirect('results','{0:.2f}'.format(estimated_damage), total_estimate)
    else:
        form = DisasterForm()

    return render(request, 'form.html', {'form': form})

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
        elif should_add_coefficient(coefficient.variable,'sewage_1',report,'sewage',1):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'minor10_1_1',report,'minor10_1',1):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'minor10_2_1',report,'minor10_2',1):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'major20_0_1',report,'major20_0',1):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'major20_1_1',report,'major20_1',1):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'major20_2_1',report,'major20_2',1):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'major30_0_1',report,'major30_0',1):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'major30_1_1',report,'major30_1',1):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'major30_2_1',report,'major30_2',1):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'major30_3_1',report,'major30_3',1):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'major40_0_1',report,'major40_0',1):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'major40_1_1',report,'major40_1',1):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'major40_2_1',report,'major40_2',1):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'major50_0_1',report,'major50_0',1):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'major50_1_1',report,'major50_1',1):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'major50_2_1',report,'major50_2',1):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'major60_0_1',report,'major60_0',1):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'major60_1_1',report,'major60_1',1):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'major74_0_1',report,'major74_0',1):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'major74_1_1',report,'major74_1',1):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'major74_2_1',report,'major74_2',1):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'destroyed80_0_1',report,'destroyed80_0',1):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'destroyed80_1_1',report,'destroyed80_1',1):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'destroyed80_2_1',report,'destroyed80_2',1):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'destroyed80_3_1',report,'destroyed80_3',1):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'destroyed80_4_1',report,'destroyed80_4',1):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'destroyed90_0_1',report,'destroyed90_0',1):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'destroyed90_1_1',report,'destroyed90_1',1):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'destroyed100_0_1',report,'destroyed100_0',1):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'destroyed100_1_1',report,'destroyed100_1',1):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'water_damage_1',report,'water_damage',1):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'water_mobilehome_1',report,'water_mobilehome',1):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'water_mobilehome_major_plywood_1',report,'water_mobilehome_major_plywood',1):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'water_mobilehome_major_nonplyw_1',report,'water_mobilehome_major_nonplywood',1):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'water_mobilehome_destroyed_1',report,'water_mobilehome_destroyed',1):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'water_conventionalhome_major_1',report,'water_conventionalhome_major',1):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif should_add_coefficient(coefficient.variable,'water_conventionalhome_destroy_1',report,'water_conventionalhome_destroyed',1):
            cur_sum+=coefficient.coefficient
            has_damage=True
        elif coefficient.variable == 'predisaster_value':
            cur_sum+=coefficient.coefficient * report.predisaster_value
        elif coefficient.variable == 'Constant':
            cur_sum+=coefficient.coefficient

    percent_damage = math.exp(cur_sum)/(1+math.exp(cur_sum)) if has_damage else 0
    estimated_damage = decimal.Decimal(percent_damage) * report.predisaster_value
    if estimated_damage > 31900: #max FEMA grant amount
        estimated_damage = 31900
    return percent_damage,estimated_damage

def should_add_coefficient(variable,var_name,report,report_var_name,report_var_value):
    return variable=='var_name' and report.get_attr(report_var_name) == report_var_value

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
        elif rand > probBig & rand <= probBig + probMed:
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


def make_report(form):
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
destroyed100_1 = form.cleaned_data['destroyed100_1'],)


def show_results(request,estimate=0.0, total = ''):
    return render(request, 'results.html',{'estimate':estimate, 'total':total})