# blog/urls.py
from django.urls import path
from . import views
from .views import (PostListView, PostDetailView, PostCreateView, PostDeleteView, PostUpdateView, CommentCreateView, CommentDeleteView, CommentUpdateView)

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
    # Comment URLs
    # Create: Linked to a specific post by its primary key (post_pk)
    path('posts/<int:post_pk>/comment/new/', CommentCreateView.as_view(), name='comment_create'),
    # Update/Delete: Linked directly to the comment's primary key (pk)
    path('comment/<int:pk>/edit/', CommentUpdateView.as_view(), name='comment_update'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
    # Search and tagging URLs
    path('search/', views.search_results, name='search'),
    path('tags/<slug:tag_slug>/', views.tagged_posts_list, name='tagged_posts'),
    
]

'''
login/
post/<int:pk>/delete/
post/<int:pk>/update/
post/new/
comment/<int:pk>/update/
post/<int:pk>/comments/new/
PostByTagListView.as_view()
'''