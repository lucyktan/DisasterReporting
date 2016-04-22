from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from Accounts.models import Account

"""
Forms for account creation and login
Modified from an opensourced project whiteboard on GitHub
"""

# creates new user
class CreateUserForm(forms.Form):
    email = forms.EmailField(label='Email',max_length=254)
    password = forms.CharField(label='Password',widget=forms.PasswordInput)
    confirmpass = forms.CharField(label='Confirm password',widget=forms.PasswordInput)
    first_name = forms.CharField(label='First name',max_length=100)
    last_name = forms.CharField(label='Last name',max_length=100)

    ##checks email and password are valid
    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        confirmpw = self.cleaned_data.get('confirmpass')
        if len(User.objects.filter(email=email)) > 0:
            raise forms.ValidationError("This email has been used")
        elif confirmpw != password:
            raise forms.ValidationError("Passwords do not match ")
        return self.cleaned_data

    ##creates new user account
    def create_new_account(self, request):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        User.objects.create_user(username=email,email=email, password=password)
        user = authenticate(email=email, password=password)
        new_account = Account(
            email=email,
            user_id=email,
            first_name=first_name,
            last_name=last_name)
        new_account.save()
        return user 

##allows user to login
class LoginForm(forms.Form):
    email = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)

    # verifies email and password information
    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(email=email, password=password,username=email)
        if not user or not user.is_active:
            raise forms.ValidationError("Incorrect Account Information")
        return self.cleaned_data

    ## lets user login to account
    def login(self, request):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(username=email, password=password)
        login(request, user)
    