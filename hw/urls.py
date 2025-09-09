# file: hw/urls.py

from django.urls import path
from django.conf import settings
from . import views # . means local directory

# URL patterns specific to the hw app:
urlpatterns = [
    # path(r'', views.home, name="home"), # connects empty string to the home function in views.py
    path(r'', views.home_page, name="home_page"),
    path(r'about', views.about, name="about_page"),
]