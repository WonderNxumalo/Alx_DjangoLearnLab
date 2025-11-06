from django.db import models
from django.contrib.auth.models import User
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
    
# UserProfile model
class UserProfile(models.Model):
    ROLE_ADMIN = 'Admin'
    ROLE_LIBRARIAN = 'Librarian'
    ROLE_MEMBER = 'Member'
    
    ROLE_CHOICES = [(ROLE_ADMIN, 'Admin'), 
                    (ROLE_LIBRARIAN, 'Librarian'), 
                    (ROLE_MEMBER, 'Member'),
                    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=ROLE_MEMBER)
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"
    
# Signal for automatic UserProfile Creation
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        instance.userprofile.save()