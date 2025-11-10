from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver

# Author Model

class Author(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
# Book Model (One-to-many relationship via foreign key)
# Book have one Author but an Author can have many books


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    
    def __str__(self):
        return self.title
    
# Library Model (Many-to-many relationship via ManyToManyField)
# A library can hold many books and books can be in many libraries

    # Custom Permission
    class Meta:
        permissions = [
            ("can_add_book", "Can add a new book to the catalog"),
            ("can_change_book", "Can edit existing book details"),
            ("can_delete_book", "Can delete a book from the catalog"),
        ]

class Library(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book)
    
    def __str__(self):
        return self.name
    
# Librarian Model (One-to-One relationship via OnetoOneField)

class Librarian(models.Model):
    name = models.CharField(max_length=100)
    library = models.OneToOneField(Library, on_delete=models.CASCADE, primary_key=True)
    
    def __str__(self):
        return self.name 
    
# Custom User Manager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)

# Custom User Model
class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.username
    
    ROLE_ADMIN = 'Admin'
    ROLE_LIBRARIAN = 'Librarian'
    ROLE_MEMBER = 'Member'
    
    ROLE_CHOICES = [
        (ROLE_ADMIN, 'Admin'),
        (ROLE_LIBRARIAN, 'Librarian'),
        (ROLE_MEMBER, 'Member'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=ROLE_MEMBER)
    
