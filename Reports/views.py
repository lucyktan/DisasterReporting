from django.shortcuts import render
from django.http import HttpResponseRedirect
from Reports.models import Report
from forms import DisasterForm

"""Renders the Report Damage form depending on whether the user is logged in"""

def get_form(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
        
    if request.method == 'POST':
        form = DisasterForm(request.POST)
        if form.is_valid():
            report=make_report(form)
            report.save()
            return HttpResponseRedirect('/results/')
    else:
        form = DisasterForm()

    return render(request, 'form.html', {'form': form})

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
major20_3 = form.cleaned_data['major20_3'],

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

destroyed90_2 = form.cleaned_data['destroyed90_0'],
destroyed100_1 = form.cleaned_data['destroyed100_1'])

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

def show_results(request):
    return render(request, 'results.html')