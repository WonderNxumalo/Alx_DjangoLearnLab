from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DeleteView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView # Use built-in CBVs
from .forms import CustomUserCreationForm, UserProfileForm, PostForm
from .models import Post # Keep Post import


# General Blog Views

def home_page(request):
    """Renders the base.html template."""
    return render(request, 'blog/base.html', {})


# CRUD Views

class PostListView(ListView):
    '''Display list of all published posts'''
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']
    
class PostDetailView(DetailView):
    '''Display single blog post.'''
    model = Post
    template_name = 'blog/post_detail.html'
    
class PostCreateView(LoginRequiredMixin, CreateView):
    '''Allow authenticated users to create new posts, setting the author automatically.'''
    model = Post
    form_class = PostForm # Use the custom form
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        # Automatically set the author to the currently logged-in user
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        # Redirect to the detail page of the new post
        return reverse('post_detail', kwargs={'pk': self.object.pk})
    
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    '''Allow the author of a post to edit it.'''
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def test_func(self):
        # UserPassesTestMixin implementation: only allow if user is the post author.
        post = self.get_object()
        return self.request.user == post.author
    
    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.pk})

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    '''Allow the author of a post to delete it.'''
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('posts') # Redirect to the post list after deletion.
    
    def test_func(self):
        # UserPassesTestMixin implementation: Only allow if the user is the post author
        post = self.get_object()
        return self.request.user == post.author

# Authentication Views

class RegisterView(CreateView):
    """Handles user registration."""
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login') # Redirect to login after successful registration
    template_name = 'blog/register.html'

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