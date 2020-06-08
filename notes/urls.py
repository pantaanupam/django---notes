from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, search

app_name = 'notes'
urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('new/', PostCreateView.as_view(), name='post-new'),
    path('<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('<int:pk>/edit/', PostUpdateView.as_view(), name='post-update'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('search/', search, name='post-search'),
]
