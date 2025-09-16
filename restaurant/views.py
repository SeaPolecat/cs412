# File: restaurant/views.py
# Author: Yi Ji (Wayne) Wang (waynew@bu.edu), 9/12/2025
# Description: Contains urls for the quotes web app that redirect to
# functions within views.py.

from django.shortcuts import render


def main(request):
    """Displays the main.html template."""

    template_name = 'restaurant/main.html'

    return render(request, template_name)


def order(request):
    """Generates a daily special item and adds it to the context, then 
    displays the order.html template.
    """


def confirmation(request):
    """Processes the submission of an order, and displays a confirmation page."""