# blog/admin.py

from django.contrib import admin

from .models import Article

# Register your models here.

# allow the django admin site to access the Article model
admin.site.register(Article)