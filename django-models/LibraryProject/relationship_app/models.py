from django.db import models

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
    
#Librarian Model (One-to-One relationship via OnetoOneField)

class Librarian(models.Model):
    name = models.CharField(max_length=100)
    library = models.OneToOneField(Library, on_delete=models.CASCADE, primary_key=True)
    
    def __str__(self):
        return self.name 
    
