# posts/serializers.py

from rest_framework import serializers
from .models import Post, Comment, Like
from accounts.serializers import ProfileSerializer # Reuse the ProfileSerializer for author/user display

# --- 1. Comment Serializer ---
class CommentSerializer(serializers.ModelSerializer):
    # Read-only field to display the commenter's username
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Comment
        # 'post' is read_only as it's set by the URL, 'user' is read_only as it's set by the request
        fields = ('id', 'post', 'user', 'user_username', 'content', 'created_at', 'updated_at')
        read_only_fields = ('post', 'user', 'created_at', 'updated_at')
        
    def create(self, validated_data):
        # The user and post are passed from the view context
        validated_data['user'] = self.context['request'].user
        validated_data['post'] = self.context['post']
        return super().create(validated_data)


# --- 2. Post Serializer ---
class PostSerializer(serializers.ModelSerializer):
    # Nested serializer to display author details (read-only)
    author_info = ProfileSerializer(source='author', read_only=True)
    # Read-only field for comment count
    comment_count = serializers.SerializerMethodField()
    # Nested representation of the first 5 comments (optional, but shows relationships)
    comments = CommentSerializer(many=True, read_only=True) 

    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'author', 'author_info', 'created_at', 'updated_at', 'comment_count', 'comments')
        # 'author' is read_only as it's set by the request, but we include it to show the ID
        read_only_fields = ('author', 'created_at', 'updated_at', 'comments')

    def get_comment_count(self, obj):
        return obj.comments.count()

    def create(self, validated_data):
        # Set the author to the currently authenticated user
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)
    
# --- Like Serializer ---
class LikeSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Like
        fields = ('id', 'post', 'user', 'user_username', 'created_at')
        read_only_fields = ('user', 'created_at')