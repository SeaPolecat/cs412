# File: mini_insta/forms.py
# Author: Yi Ji (Wayne) Wang (waynew@bu.edu), 10/3/2025
# Description: Defines the forms that we use for create/update/delete 
# operations in the Mini Insta app.

from django import forms
from .models import *


class CreatePostForm(forms.ModelForm):
    """A form to add a Post to a Mini Insta Profile."""

    class Meta:
        """Associate this form with the Post model."""

        model = Post
        fields = ['caption'] # the data we want the user to enter


class UpdateProfileForm(forms.ModelForm):
    """A form to update a Mini Insta Profile."""

    class Meta:
        """Associate this form with the Profile model."""

        model = Profile
        fields = ['display_name', 'profile_image_url', 'bio_text']