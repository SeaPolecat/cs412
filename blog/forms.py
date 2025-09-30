# blog/forms.py
# define the forms that we use for create/update/delete operations

from django import forms
from .models import Article, Comment


class CreateArticleForm(forms.ModelForm):
    """A form to add an Article to the database."""

    class Meta:
        """Associate this form with the Article model."""

        model = Article
        fields = ['author', 'title', 'text', 'image_url'] # the db can set the publish date automatically


class CreateCommentForm(forms.ModelForm):
    """A form to add a Comment about an Article."""

    class Meta:
        """Associate this form with the Comment Model."""

        model = Comment
        fields = ['author', 'text']