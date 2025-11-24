from django.db import models
from django.core.exceptions import ValidationError

# Author Model

class Author(models.Model):
    '''
    A model representing an Author (a model to store the name of the author).
    '''
    name = models.CharField(max_length=100, unique=False)
    
    def __str__(self):
        return self.name
    
# Book Model

class Book(models.Model):
    '''
    A model representing a book. ForeignKey to Author (One-to-Many relationship)
    '''
    title = models.CharField(max_length=255)
    publication_year =models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books') # Foreign key to establish One-to-Many relationship
    
    def __str__(self):
        return f"{self.title} by {self.author.name}, published: {self.publication_year}."


