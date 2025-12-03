# blog/urls.py
from django.urls import path
from . import views
from .views import (PostListView, PostDetailView, PostCreateView, PostDeleteView, PostUpdateView)

urlpatterns = [
    # Mapped views for the links in base.html
    path('', views.home_page, name='home'),
    # CRUD URLs
    path('posts/', PostListView.as_view(), name='posts'), # ListView
    path('posts/new/', PostCreateView.as_view(), name='post_create'),
    # Detail, Update, and Delete use a primary key (pk) in the URL
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'), # Detail view
    path('posts/<int:pk>/edit/', PostUpdateView.as_view(), name='post_update'), # Update view
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'), # Delete view
    # Authentication URLs
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/', views.profile_view, name='profile'),
    
]

'''
login/
post/<int:pk>/delete/
post/<int:pk>/update/
post/new/
'''