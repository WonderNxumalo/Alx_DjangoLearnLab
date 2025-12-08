from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser

# Registration Serialiser
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    
    class Meta:
        model = CustomUser
        # Fields required for registration
        fields = ('id', 'username', 'email', 'password', 'password2', 'bio', 'profile_picture')
        extra_kwargs = {'password': {'write_only': True}}
        
    def validate(self, data):
        # Ensure passwords match
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Password fields do not match."})
        return data
    
    def create(self, validated_data):
        # Remove password2 before creation
        validated_data.pop('password2')
        
        # Create user instance using the custom manager's create_user method
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            bio=validated_data.get('bio'),
            profile_picture=validated_data.get('profile_picture')
        )
        return user
    
# Login Serialiser (Token Retrieval)
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)
    
    def validate(self, data):
        username = data.get("username")
        password = data.get("password")
        
        if username and password:
            # Authenticate the user
            user = authenticate(request=self.context.get('request'),
                                username=username,
                                password=password)
            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code='authorization')
        data['user'] = user
        return data
    
# User Profile Serialiser (Read/Update)
class ProfileSerializer(serializers.ModelSerializer):
    # Use read_only fields for followers/following count 
    follower_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    
    class Meta:
        model = CustomUser
        # Fields exposed to profile view and management
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'bio', 'profile_picture', 'follower_count', 'following_count')
        read_only_fields = ('username', 'email')
        
    def get_follower_count(self, obj):
        return obj.followers.count()
    
    def get_following_count(self, obj):
        return obj.following.count()
    
'''
from rest_framework.authtoken.models import Token
Token.objects.create
get_user_model().objects.create_user
'''