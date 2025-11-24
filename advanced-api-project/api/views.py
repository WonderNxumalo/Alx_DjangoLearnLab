from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer

# Define permission classes
# A class to allow ful access (Read/Write) only to authenticated users

class IsAuthenticatedOrCreatedOnly(permissions.BasePermission):
    '''
    Custom permission to allow read-only access for anyone, but write access to authenticated users.
    '''
    def has_permission(self, request, view):
        # Allow POST and SAFE methods (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS or request.method == 'POST':
            return True
        # Deny access for all other unsafe methods (PUT, PATCH, DELETE)
        return request.user and request.user.is_authenticated

# Generic Views for Book model

# List and Create View (for GET and POST requests)
class BookListCreateAPIView(generics.ListCreateAPIView):
    '''
    View for listing all books and creating a new book. GET: retrieves a list of all books. POST: Creates a new book instance
    '''
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    # Permission setup. Allow read-only access for anyone, but write access requires authentication
    permission_classes = [IsAuthenticatedOrCreatedOnly]
    
# Detail View (for GET, PUT, PATCH, DELETE requests)
class BookRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    '''
    View for retrieving, updating, and delting a specifi book instance by primary key (pk)
    - GET: Retrieves a single Book instance. (Allowed for all users)
    - PUT/PATCH: Updates an existing Book instance. (Restricted to authenticated users)
    - DELETE: Removes a Book instance. (Restricted to authenticated users)
    '''
    
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'pk' # specifies the URL parameter to use for lookup
    
    # Permission setup: Allow read-only, but for authenticated users.
    permission_classes = [IsAuthenticatedOrCreatedOnly]
    
    '''
    ListView
    DetailView
    CreateView
    UpdateView
    DeleteView
    '''