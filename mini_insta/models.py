# File: mini_insta/models.py
# Author: Yi Ji (Wayne) Wang (waynew@bu.edu), 9/26/2025
# Description: Describes what a Profile entity should look in the database.

from django.db import models


class Profile(models.Model):
    """Encapsulate the data of a Mini Insta profile."""

    username = models.TextField(blank=True)
    display_name = models.TextField(blank=True)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateField(auto_now=True)

    def __str__(self):
        """Return a string representation of this Profile model instance."""

        return f'{self.username} ({self.display_name})'
    

class Post(models.Model):
    """Encapsulate the data of a post on a Mini Insta profile."""

    # the foreign key to indicate the relationship to the Profile of the creator of this post
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    caption = models.TextField(blank=True) # the optional text associated with this post
    timestamp = models.DateTimeField(blank=True) # the time at which this post was created/saved

    def __str__(self):
        """Return a string representation of this Post model instance."""

        return f'{self.profile}: {self.caption}'
    

class Photo(models.Model):
    """Encapsulate the data of an image on a Mini Insta post."""

    # the foreign key to indicate the relationship to the Post to which this Photo is associated
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.URLField(blank=True) # a valid URL to an image stored on the public world-wide web
    timestamp = models.DateTimeField(blank=True) # the time at which this Photo was created/saved

    def __str__(self):
        """Return a string representation of this Photo model instance."""

        return f'{self.post}: {self.image_url}'