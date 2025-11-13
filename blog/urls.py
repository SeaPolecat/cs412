# blog/urls.py

from django.urls import path
from .views import * # import ALL view classes
from django.contrib.auth import views as auth_views # generic view for authentication/authorization

urlpatterns = [
    path('', RandomArticleView.as_view(), name="random"),
    path('show_all', ShowAllView.as_view(), name="show_all"),
    path('article/create', CreateArticleView.as_view(), name='create_article'),
    path('article/<int:pk>', ArticleView.as_view(), name='article'), # display a single article based on its primary key
    path('article/<int:pk>/create_comment', CreateCommentView.as_view(), name='create_comment'), # create comment on specific article
    path('article/<int:pk>/update', UpdateArticleView.as_view(), name='update_article'), # update an article's contents
    path('comment/<int:pk>/delete', DeleteCommentView.as_view(), name='delete_comment'), # delete a comment on an article

    ## authorization-related URLs:

    # need to specify a custom template_name so Django doesn't try to use the default
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='show_all'), name='logout'), # next_page does something similar
    path('register/', UserRegistrationView.as_view(), name='register'), # create a new User account

    ## API URLs:
    path('api/articles', ArticleListAPIView().as_view()),
    path('api/article/<int:pk>', ArticleDetailAPIView().as_view()),
]