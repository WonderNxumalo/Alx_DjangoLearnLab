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