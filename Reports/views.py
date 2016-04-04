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
manufactured_minor_3=form.cleaned_data['manufactured_minor_3'],
                  latitude=lat,
                  longitude=lng)

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