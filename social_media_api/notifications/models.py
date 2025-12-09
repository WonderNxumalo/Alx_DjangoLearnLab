# notifications/models.py

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from accounts.models import CustomUser

class Notification(models.Model):
    # The user receiving the notification
    recipient = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name='notifications'
    )

    # The user who performed the action (e.g., the liker, the follower)
    actor = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name='actions'
    )

    # The description of the action (e.g., 'liked', 'commented on', 'followed')
    verb = models.CharField(max_length=255)

    # Generic Foreign Key setup to link to any object (Post, Comment, etc.)
    target_ct = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    target_id = models.PositiveIntegerField()
    target = GenericForeignKey('target_ct', 'target_id')

    timestamp = models.DateTimeField(auto_now_add=True)
    unread = models.BooleanField(default=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Notification for {self.recipient.username}: {self.actor.username} {self.verb} {self.target} "
