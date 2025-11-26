from django.contrib import admin
from .models import *


admin.site.register(Player)
admin.site.register(Box)
admin.site.register(Item)
admin.site.register(OwnedItem)
admin.site.register(DisplayItem)
admin.site.register(Trade)