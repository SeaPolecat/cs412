# blog/views.py

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Article
from .forms import CreateArticleForm, CreateCommentForm
from django.urls import reverse

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
    

# CreateView helps us create a new instance of a model data
# define a subclass of CreateView to handle creation of Article objects
class CreateArticleView(CreateView):
    """A view to handle creation of a new Article.
    
    (1) Display the HTML form to the user (GET)
    (2) Process the form submission and store the new Article object (POST)
    """

    form_class = CreateArticleForm
    template_name = 'blog/create_article_form.html'


class CreateCommentView(CreateView):
    """A view to handle creation of a new Comment on an Article."""

    form_class = CreateCommentForm
    template_name = 'blog/create_comment_form.html'


    # a different way to solve the "No URL to redirect to" error
    # (other than get_absolute_url in the model class)
    def get_success_url(self):
        """Provide a URL to redirect to after creating a new Comment."""
        
        # reverse allows us to create a and return a URL (from a URL pattern name)
        # return reverse('show_all') # not ideal; we will return to this

        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']

        # now it will redirect to the article the comment was posted on!
        # (instead of the show_all page)
        return reverse('article', kwargs={'pk': pk})
    

    def get_context_data(self):
        """Return the dictionary of context variables for use in the template."""

        # calling the superclass method
        context = super().get_context_data()

        # find/add the article to the context data
        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']

        article = Article.objects.get(pk=pk)

        # add this article into the context dictionary:
        context['article'] = article

        return context
    
    
    # override the form_valid method to attach the Article FK to the Comment instance
    def form_valid(self, form):
        """This method handles the form submission and saves the
        new object to the Django database.
        We need to add the foreign key (of the Article) to the Comment
        object before saving it to the database.
        """
        
        # shows the the data that was sent in the form submission
        print(form.cleaned_data)

        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']

        article = Article.objects.get(pk=pk)

        # attach this article to the comment;
        # instance is an instance of the Comment that was just created
        form.instance.article = article # set the FK

        # delegate the work to the superlcass method form_valid:
        return super().form_valid(form)