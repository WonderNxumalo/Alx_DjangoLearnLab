from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from .forms import CustomUserCreationForm, UserProfileForm
from .models import Post


# Create your views here.
def home_page(request):
    '''Renders the main base page.'''
    return render(request, 'base.html', {'title': 'Home'})

def post_list(request):
    '''Placeholder for listing all posts'''
    return render(request, 'base.html', {'title': 'All Blog Posts', 'content-heading': 'Blog Post List'})

# Custom Views

class RegisterView(CreateView):
    '''Handles user registration using the custom form.'''
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login') # Redirect to login on success
    template_name = 'registration/register.html'
    
    def form_valid(self, form):
        # Optional: A success message
        messages.success(self.request, "Account created successfully. Please log in.")
        return super().form_valid(form)
    
@login_required
def profile_view(request):
    '''Allows authenticated users to view and update their profile details.'''
    user = request.user
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
        else:
            form = UserProfileForm(instance=user)
            
        context = {
            'title': 'User Profile',
            'form': form,
        }
        return render(request, 'profile.html', context)