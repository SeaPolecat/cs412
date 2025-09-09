# file: quotes/views.py

from django.shortcuts import render

quotes = [
    "Halloween is my kind of a holiday... Not like those other stupid holidays. I don't get pine needles in my paws. There's no dumb bunnies, no fireworks, no relatives, just candy. Boom, you go out, you get candy. It's as simple as that.",
    "The Real World! That’s the change I need!",
    "Good morning? GOOD MORNING?! Jon, it’s Monday! Monday is the armpit of the week! It‘s like a black hole in the calendar that just sucks all the joy out of your entire being!",

]

images = [
    "https://i.guim.co.uk/img/media/6b84d191353d5f505a76c4e2bfa4caed5387d7d2/102_0_1844_1107/master/1844.jpg?width=1200&height=900&quality=85&auto=format&fit=crop&s=6b589d1a632c3af3523294eb45fd7ea2",
    "https://cdn.theatlantic.com/thumbor/J93FXmgZPJbY5FNh1FHuqgcVLQU=/1050x0:3750x2700/1080x1080/media/img/mt/2023/09/garfield_3/original.jpg",
    "https://miro.medium.com/0*vadY-LsiyPkYECZL.jpg",
]

def quote(request):
    """Display one random quote and one random image."""

    
def show_all(request):
    """Show all quotes and images."""

def about(request):
    """Display information about the famous person whose quotes are shown in this application."""