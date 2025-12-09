# File: project/admin.py
# Author: Yi Ji (Wayne) Wang (waynew@bu.edu), 12/08/2025
# Description: Register models to the Django admin site.

from django.contrib import admin
from .models import *


# register models to the Django admin site
admin.site.register(Player)
admin.site.register(Box)
admin.site.register(Item)
admin.site.register(OwnedItem)
admin.site.register(DisplayItem)
admin.site.register(Trade)