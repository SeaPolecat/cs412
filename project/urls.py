# File: project/urls.py
# Author: Yi Ji (Wayne) Wang (waynew@bu.edu), 12/08/2025
# Description: Contains urls that redirect to view classes within views.py.

from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views


urlpatterns = [

    ## URLs where login is optional

    path('', PlayerListView.as_view(), name='show_all_players'),
    path('player/<int:pk>', PlayerDetailView.as_view(), name='show_player'),
    path('player/<int:pk>/collection', ShowCollectionDetailView.as_view(), name='show_collection'),

    ## URLs where login is required

    path('player', MyPlayerDetailView.as_view(), name='show_my_player'),
    path('player/update', UpdatePlayerView.as_view(), name='update_player'),
    path('player/display/<int:slot>', DisplayCollectionView.as_view(), name='display_collection'),
    path('player/trades', ShowTradesDetailView.as_view(), name='show_trades'),
    path('player/<int:pk>/start_trade', StartTradeView.as_view(), name='start_trade'),
    path('player/trade/<int:pk>/accept', AcceptTradeView.as_view(), name='accept_trade'),
    path('player/trade/<int:pk>/reject', RejectTradeView.as_view(), name='reject_trade'),

    path('creator/boxes', BoxListView.as_view(), name='show_all_boxes'),
    path('creator/box/<int:pk>', BoxDetailView.as_view(), name='show_box'),
    path('creator/create_box', CreateBoxView.as_view(), name='create_box'),
    path('creator/box/<int:pk>/update', UpdateBoxView.as_view(), name='update_box'),
    path('creator/box/<int:pk>/delete', DeleteBoxView.as_view(), name='delete_box'),
    path('creator/box/<int:pk>/publish', PublishBoxView.as_view(), name='publish_box'),
    path('creator/box/<int:pk>/unpublish', UnpublishBoxView.as_view(), name='unpublish_box'),
    path('creator/box/<int:pk>/create_item', CreateItemView.as_view(), name='create_item'),
    path('creator/item/<int:pk>/update', UpdateItemView.as_view(), name='update_item'),
    path('creator/item/<int:pk>/delete', DeleteItemView.as_view(), name='delete_item'),

    path('shop/boxes', ShopBoxListView.as_view(), name='show_all_shop_boxes'),
    path('shop/box/<int:pk>', ShopBoxDetailView.as_view(), name='show_shop_box'),
    path('shop/box/<int:pk>/open', OpenBoxView.as_view(), name='open_box'),

    ## URLs for authentication

    path('login', auth_views.LoginView.as_view(template_name='project/login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(next_page='show_all_players'), name='logout'),
    path('create_player', CreatePlayerView.as_view(), name='create_player'),
]