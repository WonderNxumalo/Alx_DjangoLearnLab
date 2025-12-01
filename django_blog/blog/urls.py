from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('posts/', views.post_list, name='posts'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/', views.profile_view, name='profile'),
]