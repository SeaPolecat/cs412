# File: mini_insta/forms.py
# Author: Yi Ji (Wayne) Wang (waynew@bu.edu), 9/26/2025
# Description:

from django import forms
from .models import *


class CreatePostForm(forms.ModelForm):
    """A form to add a Post to a Mini Insta profile."""

    class Meta:
        """Associate this form with the Post model."""

        model = Post
        fields = ['caption']