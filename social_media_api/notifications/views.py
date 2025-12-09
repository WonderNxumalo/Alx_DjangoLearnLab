# notifications/views.py

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer
from posts.views import StandardResultsPagination # Reuse pagination

# --- /notifications/ View (GET) ---
class NotificationListView(generics.ListAPIView):
    """
    Retrieves and displays the authenticated user's notifications.
    Marks retrieved notifications as read.
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsPagination
    
    def get_queryset(self):
        # Fetch notifications for the current user, ordered newest first
        return Notification.objects.filter(recipient=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        # Calculate unread count prominently
        unread_count = queryset.filter(unread=True).count()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
        else:
            serializer = self.get_serializer(queryset, many=True)
            response = Response(serializer.data)

        # Mark all notifications shown in this list view as read
        queryset.filter(unread=True).update(unread=False)

        # Add unread count to the response data (if using custom Response)
        if isinstance(response.data, dict):
             response.data['unread_count'] = unread_count
        
        return response
