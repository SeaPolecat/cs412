# File: blog/serializers.py
# Serializers convert our django data models to a text-representation suitable to transmit over HTTP

from rest_framework import serializers # pipenv install django-rest-framework
from .models import *

class ArticleSerializer(serializers.ModelSerializer):
    """A serializer for the Article model. Specify which
    model/fields to send in the API.
    """

    class Meta:
        model = Article
        fields = ['id', 'title', 'author', 'text', 'published', 'image_file'] # id is same as pk

    # add methods to customize the Create/Read/Update/Delete operations
    def create(self, validated_data):
        """Override the superclass method that handles object creations."""

        print(f'ArticleSerializer.create, validated_data={validated_data}')

        # # create an Article object
        # article = Article(**validated_data)

        # # attach a FK for the User
        # article.user = User.objects.first()

        # # save the object to the database
        # article.save()

        # # return an object instance
        # return article
    
        ######## a simplified way:

        # attach a FK for the User
        validated_data['user'] = User.objects.first()

        # do the create and save all at once
        return Article.objects.create(**validated_data)