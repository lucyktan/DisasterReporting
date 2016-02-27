from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render 
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from DisasterReporting.forms import CreateUserForm, LoginForm

def home(request):
    return render(request, 'home.html')

def createaccount(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.create_new_account(request)
            return HttpResponseRedirect('/login/')
    else:
        form = CreateUserForm()
    return render(request, 'Accounts/createaccount.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            form.login(request)
            return HttpResponseRedirect('/home/')
    else:
        form = LoginForm()
    return render(request, 'Accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/home/')