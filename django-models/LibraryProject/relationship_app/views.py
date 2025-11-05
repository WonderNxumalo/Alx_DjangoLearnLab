from django.shortcuts import render
# from django.views.generic.detail import DetailView
# from django.contrib.auth import login
from django.views.generic import DetailView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from .models import Book, Library

# --- 1. Function-based View ---
def list_all_books(request):
    # Fetch all books from the DBs
    all_books = Book.objects.all().select_related('author')
    
    context = {'books': all_books}
    # Render list_books.html template
    # relationship_app/list_books.html
    return render(request, 'relationship_app/list_books.html', context)

# --- 2. Class-based View ---
class LibraryDefaultView(DetailView):
    model = Library
    #relationship_app/library_detail.html ( from .models import Library )
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
    
    def get_queryset(self):
        return Library.objects.all().prefetch_related('books__author', 'librarian')
    
# --- 3. Authentication Views
class CustomLoginView(LoginView):
    template_name = 'relationship_app/login.html'
    # Optional: Define where to go after successful login
    next_page = reverse_lazy('book-list')
    
class CustomLogoutView(LogoutView):
    template_name = 'relationship_app/logout.html'
    next_page = reverse_lazy('login')
    
class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'relationship_app/register.html'
    success_url = reverse_lazy('login')