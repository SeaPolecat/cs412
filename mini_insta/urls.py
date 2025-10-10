# File: mini_insta/urls.py
# Author: Yi Ji (Wayne) Wang (waynew@bu.edu), 10/3/2025
# Description: Contains urls for the Mini Instagram app that redirect to
# view classes within views.py.

from django.urls import path
from .views import *

# list containing different url endings that redirect to view classes within views.py
urlpatterns = [
    path('', ProfileListView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>', ProfileDetailView.as_view(), name='show_profile'),
    path('post/<int:pk>', PostDetailView.as_view(), name='show_post'),
    path('profile/<int:pk>/create_post', CreatePostView.as_view(), name='create_post'),
    path('profile/<int:pk>/update', UpdateProfileView.as_view(), name='update_profile'),
    path('post/<int:pk>/delete', DeletePostView.as_view(), name='delete_post'),
    path('post/<int:pk>/update', UpdatePostView.as_view(), name='update_post'),
    path('photo/<int:pk>/delete', DeletePhotoView.as_view(), name='delete_photo'),
]