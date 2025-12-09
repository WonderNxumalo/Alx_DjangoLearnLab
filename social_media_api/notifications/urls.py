# notifications/urls.py

from django.urls import path
from .views import NotificationListView

urlpatterns = [
    # Notification list endpoint
    path('', NotificationListView.as_view(), name='notification_list'),
]