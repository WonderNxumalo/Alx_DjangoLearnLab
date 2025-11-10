from django.shortcuts import render
# from django.views.generic.detail import DetailView
# from django.contrib.auth import login
# UserCreationForm()
#from django.contrib.auth.decorators import permission_required
from django.views.generic import DetailView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import user_passes_test, permission_required
from django.http import HttpResponse
from .models import Book, Library, CustomUser

# Custom Access Test Functions

def is_admin(user):
    return user.is_authenticated and user.userprofile.role == CustomUser.ROLE_ADMIN

def is_librarian(user):
    return user.is_authenticated and user.userprofile.role == CustomUser.ROLE_LIBRARIAN

def is_member(user):
    return user.is_authenticated and user.userprofile.role == CustomUser.ROLE_MEMBER


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
    
# Role-based Views (Access by Role)
@user_passes_test(is_admin, login_url='/login/')
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html', {'role': 'Admin'})

@user_passes_test(is_librarian, login_url='/login/')
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html', {'role': 'Librarian'})

@user_passes_test(is_member, login_url='/login/')
def member_view(request):
    return render(request, 'relationship_app/member_view.html', {'role': 'Member'})

# Secure Book Management Views

@permission_required('relationship_app.can_add_book', login_url='/login/')
def book_add(request):
    return HttpResponse("<h1>Add Book Page</h1><p>User has permission to add books.</p><p><a href='/books/'>Back to list</a></p>")

@permission_required('relationship_app.can_change_book', login_url='/login/')
def book_edit(request, pk):
    return HttpResponse(f"<h1>Edit Book {pk} Page</h1><p>User has permission to change books.</p><p><a href='/books/'>Back to list</a></p>")

@permission_required('relationship_app.can_delete_book', login_url='/login/')
def book_delete(request, pk):
    return HttpResponse(f"<h1>Delete Book {pk} Page</h1><p>User has permission to delete books.</p><p><a href='/books/'>Back to list</a></p>")
