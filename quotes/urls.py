# File: quotes/urls.py
# Author: Yi Ji (Wayne) Wang (waynew@bu.edu), 9/12/2025
# Description: Contains urls for the quotes web app that redirect to
# functions within views.py.

from django.urls import path
from django.conf import settings
from . import views

# list containing different url endings that redirect to functions within views.py
urlpatterns = [
    path(r'', views.quote, name="main"),
    path(r'quote', views.quote, name="quote"),
    path(r'show_all', views.show_all, name="show_all"),
    path(r'about', views.about, name="about"),
]