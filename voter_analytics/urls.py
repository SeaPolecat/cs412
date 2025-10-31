# File: voter_analytics/urls.py
# Author: Yi Ji (Wayne) Wang (waynew@bu.edu), 10/31/2025
# Description: Contains urls for the Voter Analytics app that redirect to
# view classes within views.py.

from django.urls import path
from .views import *

# URL patterns that map URLs to view classes within views.py
urlpatterns = [
	path('', VotersListView.as_view(), name='voters'),
    path('graphs', GraphsListView.as_view(), name='graphs'),
    path('voter/<int:pk>', VoterDetailView.as_view(), name='voter'),
]