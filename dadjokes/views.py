# File: dadjokes/views.py
# Author: Yi Ji (Wayne) Wang (waynew@bu.edu), 11/13/2025
# Description: Contains views for the Dadjokes app. These render templates,
# pass in context variables, and handle form submissions.

from django.views.generic import ListView, DetailView
from .models import *
import random


class JokeListView(ListView):
    """View to show all Jokes."""

    model = Joke
    template_name = 'dadjokes/show_all_jokes.html'
    context_object_name = 'jokes'


class JokeDetailView(DetailView):
    """View to show a single Joke by PK."""

    model = Joke
    template_name = 'dadjokes/show_joke.html'
    context_object_name = 'joke'


class RandomJokeDetailView(DetailView):
    """View to show a random Joke."""

    model = Joke
    template_name = 'dadjokes/show_joke.html'
    context_object_name = 'joke'

    def get_object(self):
        """Override to get a random Joke from the db."""

        jokes = Joke.objects.all()

        return random.choice(jokes)
    
    def get_context_data(self, **kwargs):
        """Override to add a random Picture to the context dict."""

        context = super().get_context_data(**kwargs)

        pictures = Picture.objects.all()
        picture = random.choice(pictures)

        context['picture'] = picture

        return context


class PictureListView(ListView):
    """View to show all Pictures."""

    model = Picture
    template_name = 'dadjokes/show_all_pictures.html'
    context_object_name = 'pictures'


class PictureDetailView(DetailView):
    """View to show a single Picture by PK."""

    model = Picture
    template_name = 'dadjokes/show_picture.html'
    context_object_name = 'picture'


###################################################################################

## REST API:
from rest_framework import generics
from .serializers import *


class JokeListAPIView(generics.ListCreateAPIView):
    """An API view to return a listing of all Jokes,
    and to create a new Joke.
    """

    queryset = Joke.objects.all()
    serializer_class = JokeSerializer


class JokeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """An API view to return a single Joke by PK."""

    queryset = Joke.objects.all() # .all() works because it secretly uses the PK in the URL
    serializer_class = JokeSerializer


class RandomJokeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """An API view to return a random Joke."""

    serializer_class = JokeSerializer

    def get_object(self):
        """Override to get a random Joke from the db."""

        jokes = Joke.objects.all()

        return random.choice(jokes)


class PictureListAPIView(generics.ListCreateAPIView):
    """An API view to return a listing of all Pictures,
    and to create a new Picture.
    """

    queryset = Picture.objects.all()
    serializer_class = PictureSerializer


class PictureDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """An API view to return a single Picture by PK."""

    queryset = Picture.objects.all()
    serializer_class = PictureSerializer


class RandomPictureDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """An API view to return a random Picture."""

    serializer_class = PictureSerializer

    def get_object(self):
        """Override to get a random Picture from the db."""

        pictures = Picture.objects.all()

        return random.choice(pictures)