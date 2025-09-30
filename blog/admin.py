# blog/admin.py

from django.contrib import admin

from .models import Article, Comment

# Register your models here.

admin.site.register(Article) # allow the django admin site to access the Article model
admin.site.register(Comment)