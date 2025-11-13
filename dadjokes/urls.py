# File: mini_insta/urls.py
# Author: Yi Ji (Wayne) Wang (waynew@bu.edu), 10/17/2025
# Description: Contains urls for the Mini Instagram app that redirect to
# view classes within views.py.

from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views


# list containing different url endings that redirect to view classes within views.py
urlpatterns = [
    # path('', ProfileListView.as_view(), name='show_all_profiles'),
]