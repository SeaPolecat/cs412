# File: mini_insta/admin.py
# Author: Yi Ji (Wayne) Wang (waynew@bu.edu), 10/3/2025
# Description: Registers Mini Insta models to the Django admin site

from django.contrib import admin
from .models import *

# register models to the Django admin site
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Photo)
admin.site.register(Follow)
admin.site.register(Comment)