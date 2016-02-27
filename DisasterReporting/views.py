from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render 
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from DisasterReporting.forms import CreateUserForm, LoginForm


def createaccount(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.create_new_account(request)
            return HttpResponseRedirect('/login/')
    else:
        form = CreateUserForm(request.POST)
    return render(request, 'Accounts/createaccount.html', {'form': form})

def success(request):
    return HttpResponse('User logged in successfully.')

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            form.login(request)
            return HttpResponseRedirect('/success/')
    else:
        form = LoginForm(request.POST)
    return render(request, 'Accounts/login.html', {'form': form})