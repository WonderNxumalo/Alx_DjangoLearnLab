# blog/forms.py
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from .models import Post, Comment

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
        
class PostForm(forms.ModelForm):
    '''Form for creating and updating Post instances, now including tags.'''
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        
class CommentForm(forms.ModelForm):
    '''Form for creating and updating Comment instances.'''
    class Meta:
        model = Comment
        # Only include content, as post and author are set in the view
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
        }
        
'''
TagWidget()
'''