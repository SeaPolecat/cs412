# File: dadjokes/models.py
# Author: Yi Ji (Wayne) Wang (waynew@bu.edu), 11/13/2025
# Description: Defines what attributes the models 
# in the database should have.

from django.db import models


# jokes from https://www.countryliving.com/life/a27452412/best-dad-jokes/

class Joke(models.Model):
    """Encapsulate the data of a Joke."""

    name = models.TextField(blank=True)
    text = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string representation of this Joke model instance."""

        return f'{self.text} - by {self.name}'


class Picture(models.Model):
    """Encapsulate the data of a Picture."""

    name = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string representation of this Picture model instance."""

        return f'Picture ({self.pk}) - by {self.name}'