# accounts/views.py

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib.auth import login
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