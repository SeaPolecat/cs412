# File: mini_insta/views.py
# Author: Yi Ji (Wayne) Wang (waynew@bu.edu), 9/26/2025
# Description: Contains views for the Mini Instagram app. These render templates 
# with entities from the database as context variables.

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Profile, Post, Photo
from .forms import CreatePostForm


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


class PostDetailView(DetailView):
    """Define a view class to show a single post in detail."""

    model = Post
    template_name = 'mini_insta/show_post.html'
    context_object_name = 'post'


class CreatePostView(CreateView):
    """A view to handle creation of a new Post on a Mini Instagram Profile."""

    form_class = CreatePostForm
    template_name = 'mini_insta/create_post_form.html'

    def get_context_data(self):
        """Return the dictionary of context variables for use in the template."""

        context = super().get_context_data()

        pk = self.kwargs['pk']

        profile = Profile.objects.get(pk=pk)

        context['profile'] = profile

        return context
    
    def form_valid(self, form):
        """Handles the form submission and saves the new object 
        to the Django database.
        """

        print(form.cleaned_data)

        post = form.instance

        profile_pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=profile_pk)
        post.profile = profile

        response = super().form_valid(form)

        photo = self.request.POST['photo']

        Photo.objects.create(post=post, image_url=photo)

        return response