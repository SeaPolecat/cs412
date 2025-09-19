# File: restaurant/views.py
# Author: Yi Ji (Wayne) Wang (waynew@bu.edu), 9/19/2025
# Description: Contains views for the restaurant web app that render templates 
# and provide them with context variables.

from django.shortcuts import render

import time
import random

# a dictionary containing special order names as keys and their descriptions as values
specials = {
    "Potion of the Ancient Scrolls": "You can read 1000 words per second, but only in Latin",
    "Potion of Chameleon Veil": "Lets you blend perfectly into your surroundings, but only if you hold your breath",
    "Potion of Echoing Laughter": "Drink it and every sound you make is followed by a chorus of giggles",
    "Potion of Withering Hour": "Grants immense strength, but you age one hour every minute it’s active",
    "Potion of the Crimson Oath": "Heals any wound instantly, but binds you to repay a mysterious blood debt",
    "Potion of Forgotten Memories": "Lets you recall any memory in vivid detail, but you forget what you were just doing",
}

# a dictionary containing item names as keys and their prices as values
item_prices = {
    "Prismatic Cream Puff": 8,
    "Moonlight Nectar": 12,
    "Frostfire Gelato": 9,
    "Whispering Almonds": 3,
}

# a dictionary containing special order items as keys and their prices as values
special_prices = {
    "Potion of the Ancient Scrolls": 35,
    "Potion of Chameleon Veil": 50,
    "Potion of Echoing Laughter": 23,
    "Potion of Withering Hour": 34,
    "Potion of the Crimson Oath": 60,
    "Potion of Forgotten Memories": 76,
}


def main(request):
    """Displays the main.html template."""

    template_name = 'restaurant/main.html' # the template to render

    return render(request, template_name)


def order(request):
    """Generates a daily special item and adds it to the context, then 
    displays the order.html template.
    """

    template_name = 'restaurant/order.html' # the template to render

    # choose a random special item to put on the menu
    special_name = random.choice(list(specials.keys())) # the special item's name
    special_description = specials[special_name] # the special item's description
    special_price = special_prices[special_name] # the special item's price

    # place variables in a context dictionary to be sent to the template
    context = {
        'special_name': special_name,
        'special_description': special_description,
        'special_price': special_price,
    }
    return render(request, template_name, context)


def confirmation(request):
    """Processes the submission of an order, and displays a confirmation page."""

    template_name = 'restaurant/confirmation.html' # the template to render

    # print(request.POST) # debugging statement

    # handle the case where the request was a POST
    if request.POST:
        # extract variables from the POST request into variables
        items = request.POST.getlist('items') # list of items ordered
        special = request.POST.get('special') # special item, if it was ordered
        instructions = request.POST.get('instructions') # special instructions entered by the user
        name = request.POST.get('name') # the user's name
        phone = request.POST.get('phone') # the user's phone number
        email = request.POST.get('email') # the user's email address

        # get the time since epoch in seconds, and add between 30-60 mins to it
        future = time.time() + random.randint(30, 60) * 60

        # plug in future to the ctime() function to get a string that
        # represents the time the user's order will be ready
        readytime = time.ctime(future)
        total_price = 0 # the total price of the user's order

        # calculate the total price by processing the items list
        # and adding the price of each item to total_price
        for item in items:
            total_price += item_prices[item]

        # if a special item was ordered, add the price of that item 
        # to total_price as well
        if special:
            total_price += special_prices[special]

        # place variables in a context dictionary to be sent to the template
        context = {
            'readytime': readytime,
            'items': items,
            'special': special,
            'instructions': instructions,
            'total_price': total_price,
            'name': name,
            'phone': phone,
            'email': email,
        }
        return render(request, template_name, context)
    
    # handle the case where the user somehow ended up at the confirmation
    # page without a POST request

    # simply render the order template again
    template_name = 'restaurant/order.html'

    return render(request, template_name)