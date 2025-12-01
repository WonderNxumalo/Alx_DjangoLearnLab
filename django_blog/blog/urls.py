# blog/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Mapped views for the links in base.html
    path('', views.home_page, name='home'),
    path('posts/', views.home_page, name='posts'),
    path('login/', views.home_page, name='login'),
    path('register/', views.home_page, name='register'),
]