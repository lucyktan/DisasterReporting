"""DisasterReporting URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
"""
from django.conf.urls import url
from django.contrib import admin
from DisasterReporting.views import home
from DisasterReporting.views import createaccount
from DisasterReporting.views import login
from DisasterReporting.views import logout_view
from DisasterReporting.views import formhistory
from Reports import views

urlpatterns = [
    url(r'^$', home),
    url(r'^home/$', home),
    url(r'^createaccount/$', createaccount),
    url(r'^login/$', login),    
    url(r'^logout/$', logout_view),
    url(r'^form/$', views.get_form),
    url(r'^results/(?P<id>\d+)', views.show_results, name='results'),
    url(r'^results/', views.show_results, name='results'),
    url(r'^form/$', views.get_form),
    url(r'^form/(?P<formid>\d+)', views.edit_form),
    url(r'^formhistory/$',formhistory),
    url(r'^summaries/',views.get_summaries)
    ]


"""
browser request -> setting ROOT_URLCONF -> urls.py -> views.py --> template
"""
