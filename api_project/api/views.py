from django.shortcuts import render
from rest_framework import generics
from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer
from rest_framework import permissions

# Create your views here.
'''
class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
'''
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def get_permissions(self):
        """
        - Authentication: Requires a valid Token (set in settings.py).
        - Permissions: Uses custom logic to restrict actions.
        
        Instantiates and returns the list of permissions that this view requires.
        We apply different permissions based on the action being performed.
        """
        # Read-only actions (list, retrieve) only require the user to be authenticated.
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [permissions.IsAuthenticated]
         
         
        # Write actions (create, update, destroy) require the user to be staff (admin).    
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            # IsAuthenticated checks for a token
            # IsAdminUser checks if the user has is_staff=True
            self.permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
        
        # For any other action (if defined), default to IsAuthenticated    
        else:
            self.permission_classes = [permissions.IsAuthenticated]
            
        return [permission() for permission in self.permission_classes]