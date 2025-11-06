# from .views import list_books 
# LibraryDetailView
# views.register
# LogoutView.as_view(template_name=)
# LoginView.as_view(template_name=)

from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.list_all_books, name='book-list'),
    path('library/<int:pk>/', views.LibraryDefaultView.as_view(), name='library-detail'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('role/admin/', views.admin_view, name="admin-view"),
    path('role/librarian/', views.librarian_view, name='librarian-view'),
    path('role/member/', views.member_view, name='member-view'),
]