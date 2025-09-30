# File: mini_insta/admin.py
# Author: Yi Ji (Wayne) Wang (waynew@bu.edu), 9/26/2025
# Description: Contains code to register models to the Django admin site

from django.contrib import admin
from .models import Profile, Post, Photo

# register models to the Django admin site
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Photo)