from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm): # Extend UserCreationForm to include the email field
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')
        
class UserProfileForm(forms.ModelForm): # User can update their profile info
    class Meta:
        model = User
        fields = ['email']