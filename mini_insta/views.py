# File: mini_insta/views.py
# Author: Yi Ji (Wayne) Wang (waynew@bu.edu), 9/26/2025
# Description: Contains views for the Mini Instagram app. These render templates 
# with entities from the database as context variables.

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Profile


class ProfileListView(ListView):
    """Define a view class to show all Mini Insta profiles."""

    model = Profile
    template_name = 'mini_insta/show_all_profiles.html'
    context_object_name = 'profiles'


class ProfileDetailView(DetailView):
    """Define a view class to show a single Mini Insta profile
    in detail.
    """

    model = Profile
    template_name = 'mini_insta/show_profile.html'
    context_object_name = 'profile'