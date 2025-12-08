# posts/permissions.py

from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors of an object to edit or delete it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner (author or user) of the object.
        # Check if the object has an 'author' (Post) or 'user' (Comment) field.
        owner = getattr(obj, 'author', None)
        if owner is None:
            owner = getattr(obj, 'user', None)

        if owner is not None:
            return owner == request.user
        
        # Fallback security if owner field is missing
        return False