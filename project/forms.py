from django import forms
from .models import *


class CreateBoxForm(forms.ModelForm):

    class Meta:

        model = Box
        fields = ['name', 'cover_image']


class CreateItemForm(forms.ModelForm):

    class Meta:

        model = Item
        fields = ['name', 'image', 'rarity']