from django.urls import path
from . import views
from .views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('players', PlayerListView.as_view(), name='show_all_players'),

    # get rid of all player pk's after implementing login/logout

    path('player/<int:pk>', PlayerDetailView.as_view(), name='show_player'),
    path('player/<int:pk>/items', OwnedItemListView.as_view(), name='show_all_owned_items'),
    path('player/<int:pk>/boxes', BoxListView.as_view(), name='show_all_boxes'),
    path('player/<int:pk>/box/<int:boxpk>', BoxDetailView.as_view(), name='show_box'),
    path('player/<int:pk>/display/<int:slot>', views.choose_display_item, name='choose_display_item'),

    # creation
    path('player/<int:pk>/boxes/create', CreateBoxView.as_view(), name='create_box'),
    path('player/<int:pk>/box/<int:boxpk>/update', UpdateBoxView.as_view(), name='update_box'),
    path('player/<int:pk>/box/<int:boxpk>/delete', DeleteBoxView.as_view(), name='delete_box'),

    path('player/<int:pk>/box/<int:boxpk>/create', CreateItemView.as_view(), name='create_item'),
    
    path('player/<int:pk>/box/<int:boxpk>/publish', views.publish_box, name='publish_box'),
    path('player/<int:pk>/box/<int:boxpk>/unpublish', views.unpublish_box, name='unpublish_box'),

    path('shop/boxes', ShopBoxListView.as_view(), name='show_all_shop_boxes'),
    path('shop/box/<int:pk>', ShopBoxDetailView.as_view(), name='show_shop_box'),
    path('shop/box/<int:pk>/open', views.open_box, name='open_box'),

    path('login', auth_views.LoginView.as_view(template_name='project/login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
]