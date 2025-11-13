# File: dadjokes/urls.py
# Author: Yi Ji (Wayne) Wang (waynew@bu.edu), 11/13/2025
# Description: Contains urls for the Dadjokes app that redirect to
# view classes within views.py.

from django.urls import path
from .views import *


urlpatterns = [
    ## Web URLs:

    path('', RandomJokeDetailView.as_view(), name='main'),
    path('random', RandomJokeDetailView.as_view(), name='show_random_joke'),

    path('jokes', JokeListView.as_view(), name='show_all_jokes'),
    path('joke/<int:pk>', JokeDetailView.as_view(), name='show_joke'),
    
    path('pictures', PictureListView.as_view(), name='show_all_pictures'),
    path('picture/<int:pk>', PictureDetailView.as_view(), name='show_picture'),

    ## API URLs:

    path('api', RandomJokeDetailAPIView.as_view()),
    path('api/random', RandomJokeDetailAPIView.as_view()),

    path('api/jokes', JokeListAPIView.as_view()),
    path('api/joke/<int:pk>', JokeDetailAPIView.as_view()),

    path('api/pictures', PictureListAPIView.as_view()),
    path('api/picture/<int:pk>', PictureDetailAPIView.as_view()),
    path('api/random_picture', RandomPictureDetailAPIView.as_view()),
]