from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse
from api.models import Author, Book

# Define the URLs we'll be testing
BOOKS_LIST_CREATE_URL = reverse('book-list-create') 

# Define a helper function for detail URL
def detail_url(book_pk):
    return reverse('book-detail-update-delete', kwargs={'pk': book_pk})

class BookAPITestCase(APITestCase):
    """
    Test suite for the BookListCreateAPIView and BookRetrieveUpdateDestroyAPIView.
    Focuses on CRUD operations, permissions, and query functionality (filtering/search/ordering).
    """

    def setUp(self):
        """Set up environment and test data for each test method."""
        # 1. Test Users for permission checks
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.unauthenticated_client = self.client # Default client (no login)
        
        # 2. Test Data
        self.author_a = Author.objects.create(name='Jane Austen')
        self.author_b = Author.objects.create(name='George Orwell')
        
        self.book1 = Book.objects.create(
            author=self.author_a, 
            title='Pride and Prejudice', 
            publication_year=1813
        )
        self.book2 = Book.objects.create(
            author=self.author_b, 
            title='1984', 
            publication_year=1949
        )
        self.book3 = Book.objects.create(
            author=self.author_a, 
            title='Emma', 
            publication_year=1815
        )

        # Base data for creating/updating a book
        self.valid_payload = {
            'title': 'New Book Title',
            'publication_year': 2023,
            'author': self.author_b.id 
        }

    # --- CRUD Tests ---

    def test_create_book_allowed_unauthenticated(self):
        """Test POST request (Create) is allowed for unauthenticated users (per custom permission)."""
        response = self.unauthenticated_client.post(BOOKS_LIST_CREATE_URL, self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4) # 3 initial + 1 created
        self.assertEqual(Book.objects.get(title='New Book Title').publication_year, 2023)

    def test_list_books_unauthenticated(self):
        """Test GET request (List) is allowed for unauthenticated users."""
        response = self.unauthenticated_client.get(BOOKS_LIST_CREATE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3) # Should return all 3 initial books

    def test_retrieve_book_unauthenticated(self):
        """Test GET request (Retrieve) is allowed for unauthenticated users."""
        response = self.unauthenticated_client.get(detail_url(self.book1.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Pride and Prejudice')
        
    # --- Permissions / Security Tests ---

    def test_update_book_unauthenticated_denied(self):
        """Test PUT request (Update) is denied for unauthenticated users."""
        # Log in the authenticated user for later update test
        self.client.login(username='testuser', password='password123') 
        
        # Create data using the authenticated client, then log out
        updated_data = {'title': 'Updated Title', 'publication_year': 2000, 'author': self.author_a.id}
        
        # Log out client and attempt update
        self.client.logout() 
        response = self.unauthenticated_client.put(detail_url(self.book1.pk), updated_data)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # Verify database change did NOT occur
        self.book1.refresh_from_db()
        self.assertNotEqual(self.book1.title, 'Updated Title')

    def test_delete_book_authenticated_allowed(self):
        """Test DELETE request is allowed for authenticated users."""
        self.client.login(username='testuser', password='password123')
        initial_count = Book.objects.count()
        response = self.client.delete(detail_url(self.book1.pk))
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), initial_count - 1)
        self.assertFalse(Book.objects.filter(pk=self.book1.pk).exists())

    # --- Filtering, Search, and Ordering Tests ---

    def test_filter_by_publication_year(self):
        """Test filtering the list by a specific publication_year."""
        url = f'{BOOKS_LIST_CREATE_URL}?publication_year=1813'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Pride and Prejudice')
    
    def test_filter_by_related_author_name(self):
        """Test filtering by the related author's name (author__name)."""
        # The query parameter needs the exact name: 'Jane Austen'
        url = f'{BOOKS_LIST_CREATE_URL}?author__name=Jane Austen'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2) # book1 and book3
        
    def test_search_by_title(self):
        """Test searching the list by a keyword in the title."""
        url = f'{BOOKS_LIST_CREATE_URL}?search=Prejudice'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Pride and Prejudice')
        
    def test_ordering_ascending_title(self):
        """Test ordering the list by title ascending (default)."""
        url = f'{BOOKS_LIST_CREATE_URL}?ordering=title'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Expected order: 1984, Emma, Pride and Prejudice
        self.assertEqual(response.data[0]['title'], '1984')
        self.assertEqual(response.data[2]['title'], 'Pride and Prejudice')

    def test_ordering_descending_year(self):
        """Test ordering the list by publication_year descending."""
        url = f'{BOOKS_LIST_CREATE_URL}?ordering=-publication_year'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Expected order: 1984 (1949), Emma (1815), Pride and Prejudice (1813)
        self.assertEqual(response.data[0]['title'], '1984')
        self.assertEqual(response.data[2]['title'], 'Pride and Prejudice')

    # --- Validation Test ---
    
    def test_create_book_invalid_future_year(self):
        """Test validation error when publication_year is in the future."""
        future_year = self.book1.publication_year + 500
        invalid_payload = {
            'title': 'Time Traveler',
            'publication_year': future_year,
            'author': self.author_a.id 
        }
        response = self.client.post(BOOKS_LIST_CREATE_URL, invalid_payload)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)
        self.assertIn('future', str(response.data['publication_year']))
        self.assertEqual(Book.objects.count(), 3) # Should not create the book