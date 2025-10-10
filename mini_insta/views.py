# File: mini_insta/views.py
# Author: Yi Ji (Wayne) Wang (waynew@bu.edu), 10/10/2025
# Description: Contains views for the Mini Insta app. These render templates,
# pass in context variables, and handle form submissions.

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Profile, Post, Photo
from .forms import CreatePostForm, UpdateProfileForm, UpdatePostForm
from django.urls import reverse


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

    def get_success_url(self):
        """Provide a URL to redirect to after creating a new Post."""

        pk = self.kwargs['pk'] # PK of the Profile associated with this Post

        # redirect to the Profile page with primary key pk
        return reverse('show_profile', kwargs={'pk': pk})

    def get_context_data(self):
        """Return the dictionary of context variables for use in the template."""

        pk = self.kwargs['pk'] # PK of the Profile associated with this Post

        # get the Profile instance using pk
        profile = Profile.objects.get(pk=pk)

        # get the context dict from the superclass, and add the Profile to it
        context = super().get_context_data()
        context['profile'] = profile

        return context
    
    def form_valid(self, form):
        """Handles the form submission and saves the new object 
        to the Django database.
        """

        # print the data the user entered (for debugging purposes)
        print(form.cleaned_data)

        post = form.instance # the Post instance being created
        profile_pk = self.kwargs['pk'] # PK of the Profile associated with this Post

        # get the Profile instance using pk
        profile = Profile.objects.get(pk=profile_pk)

        # attach the Profile's PK as a foreign key to the Post
        post.profile = profile
        post.save()

        # get the photo URL that the user entered through an explicit form
        # photo_image_url = self.request.POST['photo_image_url']

        # create a new Photo instance with the Post's PK as a foreign key, and
        # the given photo URL
        # photo = Photo(post=post, image_url=photo_image_url)
        # photo.save()

        # get a list of photo files the user uploaded
        photo_files = self.request.FILES.getlist('photo_files')

        # create a new Photo object for each file and save it to the db
        for file in photo_files:
            photo = Photo(post=post, image_file=file)
            photo.save()

        # let the superclass' form_valid() handle the rest
        return super().form_valid(form)
    

class UpdateProfileView(UpdateView):
    """View class to handle update of a Mini Instagram Profile."""

    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_insta/update_profile_form.html'


class UpdatePostView(UpdateView):
    """View class to update a Post on a Mini Instagram Profile."""

    model = Post
    form_class = UpdatePostForm
    template_name = 'mini_insta/update_post_form.html'

    def form_valid(self, form):
        """Handles the form submission and saves new Photos 
        to the Django database.
        """

        post = form.instance # the Post instance being updated

        # get a list of photo files the user uploaded
        photo_files = self.request.FILES.getlist('photo_files')

        # create a new Photo object for each file and save it to the db
        for file in photo_files:
            photo = Photo(post=post, image_file=file)
            photo.save()

        # let the superclass' form_valid() handle the rest
        return super().form_valid(form)


class DeletePostView(DeleteView):
    """View class to delete a Post on a Mini Instagram Profile."""

    model = Post
    template_name = 'mini_insta/delete_post_form.html'

    def get_success_url(self):
        """Provide a URL to redirect to after deleting a Post."""

        pk = self.kwargs['pk'] # PK of the Post being deleted

        # use pk to find the Post being deleted and its
        # associated Profile
        post = Post.objects.get(pk=pk)
        profile = post.profile

        # redirect to the Profile page with primary key pk
        return reverse('show_profile', kwargs={'pk': profile.pk})

    def get_context_data(self, **kwargs):
        """Return the dictionary of context variables for use in the template."""

        # get the context dict from the superclass
        context = super().get_context_data()

        # use the Post in the context to find its associated Profile
        profile = context['post'].profile

        # add the Profile to the context dict
        context['profile'] = profile

        return context
    

class DeletePhotoView(DeleteView):
    """View class to delete a Photo on a Mini Instagram Profile's Post."""

    model = Photo
    template_name = 'mini_insta/delete_photo_form.html'

    def get_success_url(self):
        """Provide a URL to redirect to after deleting a Photo."""

        pk = self.kwargs['pk'] # PK of the Photo being deleted

        # use pk to find the Photo being deleted and its
        # associated Post
        photo = Photo.objects.get(pk=pk)
        post = photo.post

        # redirect to the Post page with primary key pk
        return reverse('show_post', kwargs={'pk': post.pk})

    def get_context_data(self, **kwargs):
        """Return the dictionary of context variables for use in the template."""

        # get the context dict from the superclass
        context = super().get_context_data()

        # use the Photo in the context to find its associated 
        # Post and Profile
        post = context['photo'].post
        profile = post.profile

        # add the Post and Profile to the context dict
        context['post'] = post
        context['profile'] = profile

        return context