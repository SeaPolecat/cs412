# file: quotes/views.py

from django.shortcuts import render

import random

quote_list = [
    "All right, David. Let's go. To the top, then.",
    "I'm gonna take you there myself, fly you to the moon. That's a promise.",
    "I feel better in metal than in my own skin.",
    "I've never wanted any of this. You never had to save me, all I've ever wanted is for you to live.",
    "Whoa! Check this! I can feel the sun!",
    "This is it. It’s the end of the line for me. but not for you.",
    "You don't make a name as a cyberpunk by how you live... you make a name by how you die.",
    "All the same meat to me. I'll slaughter each and every one of you!",
    "You’re the guy who jumps into the fire to rescue someone, anyone, even when you know you’re gonna get burned. Just that type.",
]

image_list = [
    "https://statcdn.fandango.com/MPX/image/NBCU_Fandango/205/262/thumb_4AE07441-C039-428E-94A7-840B0943466F.jpg",
    "https://www.digitaltrends.com/wp-content/uploads/2022/09/cyberpunk-edgerunners-01.jpg?resize=1200%2C720&p=1",
    "https://cdn.mos.cms.futurecdn.net/RvsHeATNxF7B38GAEuuyNk.jpg",
    "https://i.pinimg.com/1200x/49/53/5e/49535e4f5409a2c76cb758969020fbbe.jpg",
    "https://i.pinimg.com/1200x/8f/9b/7f/8f9b7f970f302820d44501010ce2cced.jpg",
    "https://static0.cbrimages.com/wordpress/wp-content/uploads/2022/11/Adam-Smasher-Faceoff.jpg",
    "https://i.ytimg.com/vi/euJtZfiMRvg/maxresdefault.jpg",
    "https://static0.gamerantimages.com/wordpress/wp-content/uploads/2022/09/Cyberpunk-Edgerunners-David.jpg",
    "https://i.pinimg.com/1200x/39/cb/d0/39cbd09e6844b44a8c1a09996b68a2dd.jpg",
]


def quote(request):
    """Display one random quote and one random image."""

    template_name = 'quotes/quote.html'

    context = {
        'quote': random.choice(quote_list),
        'image': random.choice(image_list),
    }
    return render(request, template_name, context)

    
def show_all(request):
    """Show all quotes and images."""

    template_name = 'quotes/show_all.html'

    context = {
        'quote_list': quote_list,
        'image_list': image_list,
    }
    return render(request, template_name, context)


def about(request):
    """Display information about the famous person whose quotes are shown in this application."""

    template_name = 'quotes/about.html'

    return render(request, template_name)