# formdata/views.py

from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def show_form(request):
    """Show the form to the user."""

    template_name = 'formdata/form.html'

    return render(request, template_name)


def submit(request):
    """Process the form submission, and generate a result."""

    template_name = 'formdata/confirmation.html'

    context = {}

    # prints the POST form input as a dict
    print(request.POST)

    # check if POST data was sent with the HTTP POST message:
    if request.POST:
        # extract form fields into vars
        name = request.POST['name']
        favourite_colour = request.POST['favourite_colour']

        context['name'] = name
        context['favourite_colour'] = favourite_colour
        
    # delegate the response to the template, provide context variables
    return render(request, template_name, context)