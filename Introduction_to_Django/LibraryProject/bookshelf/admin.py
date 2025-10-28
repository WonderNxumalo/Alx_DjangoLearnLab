from django.contrib import admin
from .models import Book

# Define the custom class to manage the Book model in the Admin
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year') # Custom list display on admin list view
    list_filter = ('author', 'publication_year') # List filters (side bar filter)
    search_fields = ('title', 'author') # Configure search bar
    
# Register the Book model with the custom configuration
admin.site.register(Book, BookAdmin)
