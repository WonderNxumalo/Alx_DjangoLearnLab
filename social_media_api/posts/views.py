# posts/views.py
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, permissions, generics
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly, StandardResultsPagination # We will define this custom permission

# --- Custom Pagination Class (Step 5) ---
class StandardResultsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


# --- Post ViewSet (Step 3 & 5) ---
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = StandardResultsPagination # Pagination
    
    # Permissions: Authenticated users can create/edit/delete, others can only read
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly] 
    
    # Filtering: Allows searching by 'title' or 'content' (Step 5)
    filter_backends = [SearchFilter]
    search_fields = ['title', 'content'] 

    # We override perform_create to set the author (redundant due to serializer, but good practice)
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# --- Comment ViewSet (Step 3 & 5) ---
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = StandardResultsPagination # Pagination
    
    # Permissions: Authenticated users can create/edit/delete, others can only read
    # Use IsAuthenticated for comments to prevent anonymous comments, but IsAuthorOrReadOnly for edits
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] 

    def get_queryset(self):
        # Restrict queryset to comments associated with a specific post (if nested URL is used)
        if 'post_pk' in self.kwargs:
            return Comment.objects.filter(post_id=self.kwargs['post_pk'])
        return Comment.objects.all()

    def perform_create(self, serializer):
        # We need the post ID for creation. Assuming non-nested URL for simplicity here.
        # In a real app, this would be handled via a nested router or an explicit post_id field.
        # For this setup, we'll assume the post ID is passed in the request data, or use a simplified approach.
        
        # NOTE: For simplicity and following ModelViewSet pattern, we assume the Post ID is included
        # in the request data OR we'll use a mixin if nested routing is implemented.
        # Since we use the serializer's create method to set the user/post, this is sufficient.
        serializer.save(user=self.request.user)
        
# --- /api/feed/ View (GET) ---
class FeedView(generics.ListAPIView):
    """
    Retrieves a list of posts from users the current user is following.
    """
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsPagination

    def get_queryset(self):
        # 1. Get the list of users the current user is following
        following_users = self.request.user.following.all()

        # 2. Retrieve posts created by those users
        queryset = Post.objects.filter(author__in=following_users)

        # 3. Order by created_at (newest posts at the top)
        return queryset.order_by('-created_at')