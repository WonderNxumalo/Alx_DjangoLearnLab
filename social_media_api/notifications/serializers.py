# notifications/serializers.py

from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    # Display the actor's username
    actor_username = serializers.CharField(source='actor.username', read_only=True)

    # Display what the target object is (e.g., "Post object (5)")
    target_description = serializers.CharField(source='target.__str__', read_only=True)

    class Meta:
        model = Notification
        fields = ('id', 'actor_username', 'verb', 'target_description', 
                  'timestamp', 'unread')
        read_only_fields = ('actor_username', 'verb', 'target_description', 
                            'timestamp', 'unread')