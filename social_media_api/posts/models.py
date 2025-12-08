# posts/models.py

from django.db import models
from accounts.models import CustomUser # Import the CustomUser model

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    # ForeignKey to CustomUser for the author
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at'] # Order by newest first

    def __str__(self):
        return self.title

class Comment(models.Model):
    # ForeignKey to Post
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    # ForeignKey to CustomUser for the commenter
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at'] # Order by oldest first for comment threading

    def __str__(self):
        return f"Comment by {self.user.username} on Post {self.post.id}"
