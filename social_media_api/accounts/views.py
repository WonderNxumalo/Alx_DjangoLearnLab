# accounts/views.py
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib.auth import login
from django.shortcuts import get_object_or_404
from .serializers import RegisterSerializer, LoginSerializer, ProfileSerializer
from .models import CustomUser

# --- /accounts/register/ View (POST) ---
class RegisterView(generics.CreateAPIView):
    """
    API View for User Registration.
    """
    queryset = CustomUser.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Ensure registration returns a token on successful operation
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            "user": RegisterSerializer(user, context=self.get_serializer_context()).data,
            "token": token.key
        })


# --- /accounts/login/ View (POST) ---
class LoginView(APIView):
    """
    API View for User Login and Token Retrieval.
    """
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        login(request, user) # Optional: Use Django's session login as well
        
        # Ensure login returns a token upon successful operation
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'username': user.username,
            'user_id': user.id
        })


# --- /accounts/profile/ View (GET, PUT/PATCH) ---
class ProfileView(generics.RetrieveUpdateAPIView):
    """
    API View to retrieve and update the authenticated user's profile.
    """
    # Requires authentication
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProfileSerializer
    
    def get_object(self):
        # Ensure only the currently authenticated user's profile is returned/updated
        return self.request.user
    
# --- /accounts/follow/<int:user_pk>/ View (POST) ---
class FollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_pk):
        # 1. Get the target user to follow
        try:
            user_to_follow = CustomUser.objects.get(pk=user_pk)
        except CustomUser.DoesNotExist:
            return Response(
                {"detail": "User not found."}, 
                status=status.HTTP_404_NOT_FOUND
            )

        # 2. Prevent self-following
        if request.user.pk == user_to_follow.pk:
            return Response(
                {"detail": "You cannot follow yourself."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # 3. Add the user to the current user's 'following' list
        request.user.following.add(user_to_follow)
        return Response(
            {"detail": f"You are now following {user_to_follow.username}."}, 
            status=status.HTTP_200_OK
        )

# --- /accounts/unfollow/<int:user_pk>/ View (POST/DELETE) ---
class UnfollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_pk):
        # 1. Get the target user to unfollow
        try:
            user_to_unfollow = CustomUser.objects.get(pk=user_pk)
        except CustomUser.DoesNotExist:
            return Response(
                {"detail": "User not found."}, 
                status=status.HTTP_404_NOT_FOUND
            )

        # 2. Check if the user is currently following them
        if not request.user.following.filter(pk=user_to_unfollow.pk).exists():
             return Response(
                {"detail": f"You are not currently following {user_to_unfollow.username}."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # 3. Remove the user from the current user's 'following' list
        request.user.following.remove(user_to_unfollow)
        return Response(
            {"detail": f"You have unfollowed {user_to_unfollow.username}."}, 
            status=status.HTTP_200_OK
        )