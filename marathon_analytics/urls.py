# marathon_analytics/urls.py

from django.urls import path
from . import views 
 
urlpatterns = [
    # map the URL (empty string) to the view
	path(r'', views.ResultsListView.as_view(), name='home'),
    path(r'results', views.ResultsListView.as_view(), name='results_list'),
    path(r'result/<int:pk>', views.ResultDetailView.as_view(), name='result_detail'),
]