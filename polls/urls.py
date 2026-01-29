from django.urls import path
from . import views

app_name = 'polls'

urlpatterns = [
    path('', views.PollListView.as_view(), name='poll_list'),
    path('create/', views.PollCreateView.as_view(), name='poll_create'),
    path('<slug:slug>/', views.PollDetailView.as_view(), name='poll_detail'),
    path('<slug:slug>/edit/', views.PollUpdateView.as_view(), name='poll_edit'),
    path('<slug:slug>/delete/', views.PollDeleteView.as_view(), name='poll_delete'),
    path('<slug:slug>/vote/', views.VoteView.as_view(), name='poll_vote'),
    path('<slug:slug>/results/', views.PollResultsView.as_view(), name='poll_results'),
]
