# File: project/forms.py
# Author: Yi Ji (Wayne) Wang (waynew@bu.edu), 12/08/2025
# Description: Defines the forms that we use for CRUD operations.

from django import forms
from .models import *


class CreateUpdatePlayerForm(forms.ModelForm):
    """A form to create and/or update a Player."""

    class Meta:
        model = Player
        fields = ['username', 'profile_image']


class CreateUpdateBoxForm(forms.ModelForm):
    """A form to create and/or update a Box."""

    class Meta:
        model = Box
        fields = ['name', 'cover_image']


class CreateUpdateItemForm(forms.ModelForm):
    """A form to create and/or update an Item."""

    class Meta:
        model = Item
        fields = ['name', 'image', 'rarity']