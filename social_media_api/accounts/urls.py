# accounts/urls.py

from django.urls import path
from .views import RegisterView, LoginView, ProfileView, FollowUserView, UnfollowUserView
from rest_framework.authtoken import views as auth_views

urlpatterns = [
    # Required registration endpoint
    path('register/', RegisterView.as_view(), name='register'),
    
    # Required login endpoint (using custom LoginView to return token directly)
    path('login/', LoginView.as_view(), name='login'),
    
    # Required user profile management endpoint
    path('profile/', ProfileView.as_view(), name='profile'),
    
    # Alternative: Django REST Framework's default token endpoint (if needed)
    # path('api-token-auth/', auth_views.obtain_auth_token)
    
    # Follow Management
    path('follow/<int:user_pk>/', FollowUserView.as_view(), name='follow_user'),
    path('unfollow/<int:user_pk>/', UnfollowUserView.as_view(), name='unfollow_user'),
]
