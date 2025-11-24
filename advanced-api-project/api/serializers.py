from rest_framework import serializers
from django.utils import timezone
from .models import Author, Book

# Author serialier (for nesting)

class BookSerializer(serializers.ModelSerializer):
    '''
    Serialiser for book model, includes custom validation for publication year
    '''
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']
        
    def validate_publication_year(self, value):
        '''
        Custom validation to ensure publication year isn't in the future.
        '''
        current_year = timezone.now().year
        if value > current_year:
            raise serializers.ValidationError(f"Publication year cannot be in the future. Current year is {current_year}.")
        return value
    
# Author serialiser (main serialiser)

class AuthorSerializer(serializers.ModelSerializer):
    '''
    Serialiser for the Author model. Uses a nested BookSerializer to dynamically include all related books, (one-to-many relationship)
    '''
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books']