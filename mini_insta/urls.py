# File: mini_insta/urls.py
# Author: Yi Ji (Wayne) Wang (waynew@bu.edu), 10/17/2025
# Description: Contains urls for the Mini Instagram app that redirect to
# view classes within views.py.

from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

# app_name = 'mini_insta' # could add a namespace to uniquely identify similar URLs across apps

# list containing different url endings that redirect to view classes within views.py
urlpatterns = [

    ## URLs for NOT authenticated users

    path('', ProfileListView.as_view(), name='show_all_profiles'),

    path('profile/<int:pk>', ProfileDetailView.as_view(), name='show_profile'),
    path('profile/<int:pk>/followers', ShowFollowersDetailView.as_view(), name='show_followers'),
    path('profile/<int:pk>/following', ShowFollowingDetailView.as_view(), name='show_following'),

    path('post/<int:pk>', PostDetailView.as_view(), name='show_post'),

    ## URLs for authenticated users

    path('profile/', MyProfileDetailView.as_view(), name='my_profile'),
    path('profile/create_post', CreatePostView.as_view(), name='create_post'),
    path('profile/update', UpdateProfileView.as_view(), name='update_profile'),
    path('profile/feed', PostFeedListView.as_view(), name='show_feed'),
    path('profile/search', SearchView.as_view(), name='search'),
    path('profile/<int:pk>/follow', FollowProfileView.as_view(), name='follow_profile'),
    path('profile/<int:pk>/unfollow', UnfollowProfileView.as_view(), name='unfollow_profile'),

    path('post/<int:pk>/update', UpdatePostView.as_view(), name='update_post'),
    path('post/<int:pk>/delete', DeletePostView.as_view(), name='delete_post'),
    path('post/<int:pk>/like', LikePostView.as_view(), name='like_post'),
    path('post/<int:pk>/unlike', UnlikePostView.as_view(), name='unlike_post'),

    path('photo/<int:pk>/delete', DeletePhotoView.as_view(), name='delete_photo'),

    ## authentication URLs

    path('login/', auth_views.LoginView.as_view(template_name='mini_insta/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='show_all_profiles'), name='logout'),
    path('create_profile/', CreateProfileView.as_view(), name='create_profile'),
]