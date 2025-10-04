# blog/urls.py

from django.urls import path
from .views import * # import ALL view classes

urlpatterns = [
    path('', RandomArticleView.as_view(), name="random"),
    path('show_all', ShowAllView.as_view(), name="show_all"),
    path('article/create', CreateArticleView.as_view(), name='create_article'),
    path('article/<int:pk>', ArticleView.as_view(), name='article'), # display a single article based on its primary key
    path('article/<int:pk>/create_comment', CreateCommentView.as_view(), name='create_comment'), # create comment on specific article
    path('article/<int:pk>/update', UpdateArticleView.as_view(), name='update_article'), # update an article's contents
    path('comment/<int:pk>/delete', DeleteCommentView.as_view(), name='delete_comment') # delete a comment on an article
]