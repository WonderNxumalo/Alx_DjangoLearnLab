from django.shortcuts import render
from django.views.generic import DetailView
from .models import Book, Library

# --- 1. Function-based View ---
def list_all_books(request):
    # Fetch all books from the DBs
    all_books = Book.objects.all().select_related('author')
    
    context = {'books': all_books}
    # Render list_books.html template
    # relationship_app/list_books.html
    return render(request, 'list_books.html', context)

# --- 2. Class-based View ---
class LibraryDefaultView(DetailView):
    model = Library
    #relationship_app/library_detail.html ( from .models import Library )
    template_name = 'library_detail.html'
    context_object_name = 'library'
    
    def get_queryset(self):
        return Library.objects.all().prefetch_related('books__author', 'librarian')