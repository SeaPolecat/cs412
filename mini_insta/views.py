# File: mini_insta/views.py
# Author: Yi Ji (Wayne) Wang (waynew@bu.edu), 10/17/2025
# Description: Contains views for the Mini Insta app. These render templates,
# pass in context variables, and handle form submissions.

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import *
from .forms import *
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login


class MyLoginRequiredMixin(LoginRequiredMixin):
    """My own subclass of the LoginRequiredMixin, which implements
    some useful features.
    """

    def get_login_url(self):
        """Return the URL for this app's login page."""
        return reverse('login')
    
    def get_logged_in_profile(self):
        """Return the Profile corresponding to the logged in User."""
        return Profile.objects.get(user=self.request.user)


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

    def get_context_data(self, **kwargs):
        """Return the dictionary of context variables for use in the template."""

        # get the Profile specified in the URL
        context = super().get_context_data(**kwargs)
        profile = context['profile']

        # get the logged in Profile if the user is authenticated
        if self.request.user.is_authenticated:
            my_profile = self.request.user.profile

            # set a boolean context variable to true or false depending on 
            # if the logged in Profile follows the URL Profile
            if my_profile.already_followed(profile):
                context['already_followed'] = True
            else:
                context['already_followed'] = False

        return context


class MyProfileDetailView(MyLoginRequiredMixin, DetailView):
    """View class to display a logged in user's own Profile."""

    model = Profile
    template_name = 'mini_insta/show_profile.html'
    context_object_name = 'profile'

    def get_object(self):
        """Returns the model instance to be used as a context variable."""

        return self.get_logged_in_profile()


class PostDetailView(DetailView):
    """Define a view class to show a single post in detail."""

    model = Post
    template_name = 'mini_insta/show_post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        """Return the dictionary of context variables for use in the template."""

        # get the Post specified in the URL
        context = super().get_context_data(**kwargs)
        post = context['post']

        # get the logged in Profile if the user is authenticated
        if self.request.user.is_authenticated:
            my_profile = self.request.user.profile

            # set a boolean context variable to true or false depending on 
            # if the logged in Profile has liked the URL Post
            if my_profile.already_liked(post):
                context['already_liked'] = True
            else:
                context['already_liked'] = False

        return context


class CreatePostView(MyLoginRequiredMixin, CreateView):
    """A view to handle creation of a new Post on a Mini Instagram Profile."""

    form_class = CreatePostForm
    template_name = 'mini_insta/create_post_form.html'

    def get_success_url(self):
        """Provide a URL to redirect to after creating a new Post."""

        # redirect to the logged in user's profile page
        return reverse('my_profile')
    
    def form_valid(self, form):
        """Handles the form submission and saves the new object 
        to the Django database.
        """

        # print the data the user entered (for debugging purposes)
        print(form.cleaned_data)

        post = form.instance # the Post instance being created
        my_profile = self.get_logged_in_profile()

        # attach the Profile's PK as a foreign key to the Post
        post.profile = my_profile
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
    

class UpdateProfileView(MyLoginRequiredMixin, UpdateView):
    """View class to handle update of a Mini Instagram Profile."""

    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_insta/update_profile_form.html'

    def get_object(self):
        """Returns the model instance to be used as a context variable."""

        return self.get_logged_in_profile()


class UpdatePostView(MyLoginRequiredMixin, UpdateView):
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


class DeletePostView(MyLoginRequiredMixin, DeleteView):
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

        # redirect to the Profile page whose Post was deleted
        return reverse('show_profile', kwargs={'pk': profile.pk})
    

class DeletePhotoView(MyLoginRequiredMixin, DeleteView):
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

        # redirect to the Post page whose Photo was deleted
        return reverse('show_post', kwargs={'pk': post.pk})

    def get_context_data(self, **kwargs):
        """Return the dictionary of context variables for use in the template."""

        # get the context dict from the superclass
        context = super().get_context_data()

        # use the Photo in the context to find its associated 
        # Post and Profile
        post = context['photo'].post

        # add the Post and Profile to the context
        context['post'] = post

        return context
    

class ShowFollowersDetailView(DetailView):
    """View class to show a Mini Insta profile's followers."""

    model = Profile
    template_name = 'mini_insta/show_followers.html'
    context_object_name = 'profile'


class ShowFollowingDetailView(DetailView):
    """View class to show a Mini Insta profile's following."""

    model = Profile
    template_name = 'mini_insta/show_following.html'
    context_object_name = 'profile'


class PostFeedListView(MyLoginRequiredMixin, ListView):
    """View class to display a list of Posts in the feed."""

    model = Post
    template_name = 'mini_insta/show_feed.html'
    context_object_name = 'post_feed'

    def get_queryset(self):
        """Returns a queryset that gets passed in as a context variable
        and becomes associated with context_object_name.
        """

        # get the logged in user's Profile
        my_profile = self.get_logged_in_profile()

        # get the Profile's post feed
        post_feed = my_profile.get_post_feed()

        return post_feed
    

class SearchView(MyLoginRequiredMixin, ListView):
    """View class to display a template for the user to enter search
    queries, and another template containing the search results.
    """

    model = Profile
    template_name = 'mini_insta/search_results.html'
    context_object_name = 'matching_profiles'

    def dispatch(self, request, *args, **kwargs):
        """Handles HTTP requests from the user that get mapped to
        this view through a URL.
        """

        # since i already override dispatch here, i need to manually redirect to the login page
        if not request.user.is_authenticated:
            template_name = 'mini_insta/login.html'
            context = {'form': AuthenticationForm}

            return render(request, template_name, context)

        # if the GET request contains no data, render the search.html template
        # to prompt the user to enter a search query
        if not request.GET:
            template_name = 'mini_insta/search.html' # name of the template to render

            return render(request, template_name)

        # otherwise, let the superclass' dispatch method handle the rest
        else:
            return super().dispatch(request, *args, **kwargs)
        
    def get_queryset(self):
        """Returns a queryset that gets passed in as a context variable
        and becomes associated with context_object_name.
        """

        # get the search query attached to the GET request;
        # data sent to the server via a GET request is appended to the 
        # end of the URL (can see it in browser!), unlike POST which gives a dict
        query = self.request.GET.get('query')

        # # get a list of Profiles that match the search query,
        # i.e. the query is found in its username, display name, or bio text
        matching_profiles = (
            Profile.objects.filter(username__contains=query) | # union operator that combines querysets
            Profile.objects.filter(display_name__contains=query) |
            Profile.objects.filter(bio_text__contains=query)
        )
        return matching_profiles

    def get_context_data(self, **kwargs):
        """Return the dictionary of context variables for use in the template."""

        # get the search query attached to the GET request
        query = self.request.GET.get('query')

        # get a list of Posts that match the search query,
        # i.e. the query is found in its caption
        matching_posts = Post.objects.filter(caption__contains=query)

        # get the context dict from the superclass, and add all the
        # relevant data to it
        # (I didn't add matching_profiles because it's already associated with 
        # the context_object_name as a result of overriding get_queryset)
        context = super().get_context_data()
        context['query'] = query
        context['matching_posts'] = matching_posts

        return context
    

class CreateProfileView(CreateView):
    """View class to handle creating a new Profile."""

    model = User
    form_class = CreateProfileForm
    template_name = 'mini_insta/create_profile_form.html'

    def get_context_data(self, **kwargs):
        """Return the dictionary of context variables for use in the template."""

        # add Django's user creation form into the context
        context = super().get_context_data()
        context['django_form'] = UserCreationForm

        return context
    
    def form_valid(self, form):
        """Handles the form submission and saves the new object 
        to the Django database.
        """

        # rebuild Django's user creation form
        django_form = UserCreationForm(self.request.POST)

        # save the new user to the db, and log them in
        user = django_form.save()
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')

        # attach the user as a FK to the Profile
        profile = form.instance
        profile.user = user

        return super().form_valid(form)
    

class FollowProfileView(MyLoginRequiredMixin, TemplateView):
    """View class to handle following another Profile."""

    def dispatch(self, request, *args, **kwargs):
        """Handles HTTP requests from the user that get mapped to
        this view through a URL.
        """

        # get the Profile specified in the URL
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)

        # get the logged in Profile
        my_profile = self.get_logged_in_profile()

        # if the logged in Profile isn't viewing itself, AND is not already
        # following the URL Profile, create and save a new Follow instance
        if my_profile != profile and not my_profile.already_followed(profile):
            follow = Follow(profile=profile, follower_profile=my_profile)
            follow.save()

        # redirect to the show_profile page
        return redirect('show_profile', pk=pk)
    

class UnfollowProfileView(MyLoginRequiredMixin, TemplateView):
    """View class to handle unfollowing another Profile."""

    def dispatch(self, request, *args, **kwargs):
        """Handles HTTP requests from the user that get mapped to
        this view through a URL.
        """

        # get the Profile specified in the URL
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)

        # get the logged in Profile
        my_profile = self.get_logged_in_profile()

        # get the Follow instance (if it exists)
        follow = my_profile.already_followed(profile)

        # if it exists, delete it
        if follow:
            follow.delete()

        # redirect to the show_profile page
        return redirect('show_profile', pk=pk)
    

class LikePostView(MyLoginRequiredMixin, TemplateView):
    """View class to handle liking a Post."""

    def dispatch(self, request, *args, **kwargs):
        """Handles HTTP requests from the user that get mapped to
        this view through a URL.
        """

        # get the Post specified in the URL
        pk = self.kwargs['pk']
        post = Post.objects.get(pk=pk)

        # get the logged in Profile
        my_profile = self.get_logged_in_profile()

        # if the logged in Profile isn't viewing its own Post, AND has not 
        # already liked the URL Post, create and save a new Like instance
        if my_profile != post.profile and not my_profile.already_liked(post):
            like = Like(post=post, profile=my_profile)
            like.save()

        # redirect to the show_post page
        return redirect('show_post', pk=pk)
    

class UnlikePostView(MyLoginRequiredMixin, TemplateView):
    """View class to handle unliking a Post."""

    def dispatch(self, request, *args, **kwargs):
        """Handles HTTP requests from the user that get mapped to
        this view through a URL.
        """

        # get the Post specified in the URL
        pk = self.kwargs['pk']
        post = Post.objects.get(pk=pk)

        # get the logged in Profile
        my_profile = self.get_logged_in_profile()

        # get the Like instance (if it exists)
        like = my_profile.already_liked(post)

        # if it exists, delete it
        if like:
            like.delete()

        # redirect to the show_post page
        return redirect('show_post', pk=pk)