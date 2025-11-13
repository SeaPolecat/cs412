# File: dadjokes/serializers.py
# Author: Yi Ji (Wayne) Wang (waynew@bu.edu), 11/13/2025
# Description: Defines serializers to convert our django data models 
# to a text-representation suitable to transmit over HTTP.

from rest_framework import serializers
from .models import *


class JokeSerializer(serializers.ModelSerializer):
    """A serializer for the Joke model."""

    class Meta:
        """Specify which model/fields to send in the API."""

        model = Joke
        fields = ['id', 'name', 'text', 'timestamp']


class PictureSerializer(serializers.ModelSerializer):
    """A serializer for the Picture model."""

    class Meta:
        """Specify which model/fields to send in the API."""

        model = Picture
        fields = ['id', 'name', 'image_url', 'timestamp']