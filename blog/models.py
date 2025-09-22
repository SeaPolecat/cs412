# blog/models.py
# define data models for the blog application

from django.db import models

# Create your models here.

class Article(models.Model):
    """Encapsulate the data of a blog Article by an author."""

    # need to run makemigrations and migrate every time these model vars are changed!!

    # define the data attributes of the Article object
    title = models.TextField(blank=True)
    author = models.TextField(blank=True)
    text = models.TextField(blank=True)
    published = models.DateTimeField(auto_now=True) # automatically sets published to the current time
    image_url = models.URLField(blank=True) # holds any kind of url

    def __str__(self):
        """Return a string representation of this model instance."""

        return f'{self.title} by {self.author}'