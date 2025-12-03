from django.urls import path
from . import views
from .views import *


urlpatterns = [
    path('players', PlayerListView.as_view(), name='show_all_players'),
    path('player/<int:pk>', PlayerDetailView.as_view(), name='show_player'),
    path('player/<int:pk>/items', OwnedItemListView.as_view(), name='show_all_owned_items'),
    path('player/<int:pk>/display/<int:slot>', views.choose_display_item, name='choose_display_item'),

    path('boxes', BoxListView.as_view(), name='show_all_boxes'),
    path('box/<int:pk>', BoxDetailView.as_view(), name='show_box'),
    path('box/<int:pk>/open', OpenBoxView.as_view(), name='open_box'),
]