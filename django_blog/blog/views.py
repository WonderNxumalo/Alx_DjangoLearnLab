from django.shortcuts import render

def home_page(request):
    """Renders the base.html template."""
    return render(request, 'base.html', {})
