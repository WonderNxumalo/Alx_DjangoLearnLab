from django.shortcuts import render

# Create your views here.
def home_page(request):
    '''Renders the main base page.'''
    
    context = {
        'title' : 'Welcome to Wonder',
    }
    
    return render(request, 'base.html', context)