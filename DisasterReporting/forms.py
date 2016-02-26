from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class CreateUserForm(forms.Form):
    email = forms.EmailField(max_length=254)password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirmpass = forms.CharField(widget=forms.PasswordInput, required=True)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

    def clean(self):
    	email = self.cleaned_data.get('email')
    	password = self.cleaned_data.get('password')
    	confirmpw = self.cleaned_data.get('confirmpw')
    	if len(User.objects.filter(email=email)) > 0:
    		raise forms.ValidationError("This email has been used")
    	else if confirmpw != password: 
    		raise forms.ValidationError("Passwords do not match")
    	return self.cleaned_data

    def create_new_account(self, request):
    	email = self.cleaned_data.get('email')
    	password = self.cleaned_data.get('password')
    	first_name = self.cleaned_data.get('first_name')
    	last_name = self.cleaned_data.get('last_name')
    	User.objects.create_user(email=email, password=password)
    	user = authenticate(email=email, password=password)
    	new_account = Account(
    		email=email,
    		first_name=first_name,
    		last_name=last_name)
    	new_account.save()
    	return user 

class LoginForm(forms.Form):
	email = forms.CharField(max_length=255, required=True)
	password = forms.CharField(widget=forms.PasswordInput, required=True)

	def clean(self):
		email = self.cleaned_data.get('email')
		password = self.cleaned_data.get('password')
		user = authenticate(email=email, password=password)
		if not user or not user.is_active:
			raise forms.ValidationError("Incorrect Account Information")
		return self.cleaned_data

	def login(self, request):
		email = self.cleaned_data.get('email')
		password = self.cleaned_data.get('password')
		user = authenticate(email=email, password=password)
		return user 