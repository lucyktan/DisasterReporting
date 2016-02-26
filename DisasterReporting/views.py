from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render 
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
 
def createaccount(request):
	form = CreateUserForm(request.POST or None)
	if request.POST and form.is_valid():
		user = form.create_new_account(request)
		if user is not None:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect(redirect)
	return render(request, 'Accounts/createaccount.html', {})
    