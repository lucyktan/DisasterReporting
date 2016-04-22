from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render 
from django.contrib.auth import login as django_login, logout
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from DisasterReporting.forms import CreateUserForm, LoginForm
from Reports.models import Report
import datetime
from Reports.views import total_disaster_estimate

"""
Page routing and redirecting for the home page, account creation, login, and logout
"""

##redirects user to the home screen
def home(request):
    return render(request, 'home.html')

##redirects user to the login page if account creation was successful or to the account creation page if
##account creation failed
def createaccount(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.create_new_account(request)
            new_user = authenticate(username=form.cleaned_data['email'],
                                    password=form.cleaned_data['password'],
                                    )
            django_login(request, new_user)
            return HttpResponseRedirect('/home/')
    else:
        form = CreateUserForm()
    return render(request, 'Accounts/createaccount.html', {'form': form})

##redirects user to the home page if login was successful of the login page if login failed
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            form.login(request)
            return HttpResponseRedirect('/home/')
    else:
        form = LoginForm()
    return render(request, 'Accounts/login.html', {'form': form})

##logs out user and directs them to the home screen
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/home/')

##redirects user to the formhistory page or the login page if the user is not logged in
def formhistory(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    reports = Report.objects.filter(username=request.user.username)
    for report in reports:
        report.date_num=(report.date_of_disaster-datetime.datetime.utcfromtimestamp(0).date()).days
        report.total_damage=total_disaster_estimate(report)
    return render(request,'Accounts/formhistory.html',{'reports':reports})