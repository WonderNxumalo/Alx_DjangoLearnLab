from django.contrib import admin
from .models import Book

# Define the custom class to manage the Book model in the Admin
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year') # Custom list display on admin list view
    list_filter = ('author', 'publication_year') # List filters (side bar filter)
    search_fields = ('title', 'author') # Configure search bar
    
# Register the Book model with the custom configuration
admin.site.register(Book, BookAdmin)

'''
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Author, Book, Library, Librarian


# Custom Admin for CustomerUser

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'role')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'role')
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('date_of_birth', 'profile_photo', 'role')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('date_of_birth', 'profile_photo', 'role')}),
    )
    
# Register the Customer model with its custom admin class
admin.site.register(CustomUser, CustomUserAdmin)

# Register existing app models
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Librarian)
admin.site.register(Library)
'''
