from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView # Use built-in CBVs
from .forms import CustomUserCreationForm, UserProfileForm
from .models import Post # Keep Post import

# General Blog Views

def home_page(request):
    """Renders the base.html template."""
    return render(request, 'base.html', {})

def post_list(request):
    '''Placeholder view for the list of all posts.'''
    return render(request, 'base.html', {'title': 'All Blog Posts'})

# Authentication Views

class RegisterView(CreateView):
    """Handles user registration."""
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login') # Redirect to login after successful registration
    template_name = 'registration/register.html'

    def form_valid(self, form):
        messages.success(self.request, 'Account created successfully! Please log in.')
        return super().form_valid(form)

@login_required 
def profile_view(request):
    """Allows authenticated users to view and update their profile details."""
    user = request.user
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user)
        
    context = {
        'title': 'User Profile',
        'form': form,
    }
    return render(request, 'profile.html', context)