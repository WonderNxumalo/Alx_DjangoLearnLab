from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=100)
    publication_date = models.DateField(null=True, blank=True)
    is_available = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['title']
        
    def __str__(self):
        return f"{self.title} by {self.author}"