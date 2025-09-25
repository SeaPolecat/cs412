# mini_insta/models.py

from django.db import models

class Profile(models.Model):
    """Encapsulate the data of a Mini Insta profile."""

    username = models.TextField(blank=True)
    display_name = models.TextField(blank=True)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateField(auto_now=True)

    def __str__(self):
        """Return a string representation of the Profile model instance."""

        return f'{self.username} (joined on {self.join_date})'