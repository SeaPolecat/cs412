# blog/models.py
# define data models for the blog application

from django.db import models
from django.urls import reverse

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
    

    # we need this because after submitting the form to create a new Article, there's 
    # no URL to redirect to to display it!
    def get_absolute_url(self):
        """Return a URL to display 1 instance of this object."""

        # reverses to the article URL after submitting the form;
        # self.pk is an attribute of this object storing its PK, which we pass
        # into the kwargs (keyword arguments) dict to display that article
        return reverse('article', kwargs={'pk': self.pk})
    

    def get_all_comments(self):
        """Return a QuerySet of comments about this article."""

        # use the object manager to retrieve comments about this article
        # look for comments whose foreign key is this instance of Article
        comments = Comment.objects.filter(article=self)

        return comments
    

class Comment(models.Model):
    """Encapsulate the data of a Comment about an Article."""

    # data attributes for the Comment:
    article = models.ForeignKey(Article, on_delete=models.CASCADE) # cascade delete to remove all comments if an article is deleted
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a string representation of this comment."""

        return f'{self.text}'