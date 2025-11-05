# from .views import list_books 
# LibraryDetailView

from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.list_all_books, name='book-list'),
    path('library/<int:pk>/', views.LibraryDefaultView.as_view(), name='library-detail'),
]