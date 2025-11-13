# File: dadjokes/admin.py
# Author: Yi Ji (Wayne) Wang (waynew@bu.edu), 11/13/2025
# Description: Registers models to the Django admin site.

from django.contrib import admin
from .models import *


admin.site.register(Joke)
admin.site.register(Picture)