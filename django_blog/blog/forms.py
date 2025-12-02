# blog/forms.py
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    """Extends UserCreationForm to explicitly include the email field."""
    class Meta:
        model = User
        # Ensure 'email' is included in the fields
        fields = ('username', 'email', 'password', 'password2')

class UserProfileForm(forms.ModelForm):
    """Form for users to update their profile information (email only for now)."""
    class Meta:
        model = User
        fields = ['email'] # User can change their email