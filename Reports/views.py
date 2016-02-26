from django.shortcuts import render
from django.http import HttpResponseRedirect

from Reports.models import Report
from forms import DisasterForm

def get_form(request):
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
normal_water=form.cleaned_data['normal_water'],
normal_destroyed_0=form.cleaned_data['normal_destroyed_0'],
normal_destroyed_1=form.cleaned_data['normal_destroyed_1'],
normal_destroyed_2=form.cleaned_data['normal_destroyed_2'],
normal_destroyed_3=form.cleaned_data['normal_destroyed_3'],
normal_major_0=form.cleaned_data['normal_major_0'],
normal_major_1=form.cleaned_data['normal_major_1'],
normal_major_2=form.cleaned_data['normal_major_2'],
normal_major_3=form.cleaned_data['normal_major_3'],
normal_minor_0=form.cleaned_data['normal_minor_0'],
normal_minor_1=form.cleaned_data['normal_minor_1'],
normal_minor_2=form.cleaned_data['normal_minor_2'],
normal_minor_3=form.cleaned_data['normal_minor_3'],
manufactured_destroyed_0=form.cleaned_data['manufactured_destroyed_0'],
manufactured_destroyed_1=form.cleaned_data['manufactured_destroyed_1'],
manufactured_destroyed_2=form.cleaned_data['manufactured_destroyed_2'],
manufactured_destroyed_3=form.cleaned_data['manufactured_destroyed_3'],
manufactured_major_0=form.cleaned_data['manufactured_major_0'],
manufactured_major_1=form.cleaned_data['manufactured_major_1'],
manufactured_major_2=form.cleaned_data['manufactured_major_2'],
manufactured_major_3=form.cleaned_data['manufactured_major_3'],
manufactured_minor_0=form.cleaned_data['manufactured_minor_0'],
manufactured_minor_1=form.cleaned_data['manufactured_minor_1'],
manufactured_minor_2=form.cleaned_data['manufactured_minor_2'],
manufactured_minor_3=form.cleaned_data['manufactured_minor_3'])

def show_results(request):
    return render(request, 'results.html')