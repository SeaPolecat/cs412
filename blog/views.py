# blog/views.py

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Article
import random

# Create your views here.

# generic view for looking at all instances of a model (produces a list)

class ShowAllView(ListView):
    """Define a view class to show all blog Articles."""

    model = Article
    template_name = 'blog/show_all.html'
    context_object_name = 'articles' # convention: plural and very similar to the model name


class ArticleView(DetailView):
    """Display a single article."""

    model = Article
    template_name = 'blog/article.html'
    context_object_name = 'article' # note singular var name


class RandomArticleView(DetailView):
    """Display a single article selected at random."""

    model = Article
    template_name = 'blog/article.html'
    context_object_name = 'article' # note singular var name

    # methods

    # override the default get_object method
    def get_object(self):
        """Return 1 instance of the Article object
        selected at random.
        """

        # returns a query of all articles
        all_articles = Article.objects.all()
        article = random.choice(all_articles)

        return article