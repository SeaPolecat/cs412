# File: restaurant/urls.py
# Author: Yi Ji (Wayne) Wang (waynew@bu.edu), 9/12/2025
# Description: Contains urls for the quotes web app that redirect to
# functions within views.py.

from django.urls import path
from django.conf import settings
from . import views

# list containing different url endings that redirect to functions within views.py
urlpatterns = [
    path(r'main', views.main, name="main"),
    path(r'order', views.order, name="order"),
    path(r'confirmation', views.confirmation, name="confirmation"),
]