# This script is intended to be run inside the Django shell:
# 1. python manage.py shell
# 2. exec(open('relationship_app/query_samples.py').read())


from relationship_app.models import Author, Book, Library, Librarian

print("-" * 50)
print("SETUP: Creating sample data...")
print("-" * 50)

# Author creation
author1, created = Author.objects.get_or_create(name="Jane Austen")
author2, created = Author.objects.get_or_create(name="George Orwell")
print(f"Author 1: {author1.name}")
print(f"Author 2: {author2.name}")

# Book creation (Foreign Key, one-to-many relationship)
book1, created = Book.objects.get_or_create(title="Pride and Prejudice", author=author1)
book2, created = Book.objects.get_or_create(title="Sense and Sensibility", author=author1)
book3, created = Book.objects.get_or_create(title="1984", author=author2)
print(f"Book 1: {book1.title}")
print(f"Book2: {book2.title}")
print(f"Book3: {book3.title}")

# Libraries creation (many-to-many relationship)
library_tshwane, created = Library.objects.get_or_create(name="Tshwane Library")
library_mamelodi, created = Library.objects.get_or_create(name="Mamelodi Library")
print(f"Library 1: {library_tshwane.name}")
print(f"Library 2: {library_mamelodi.name}")

# Adding books to libraries (many-to-many relationship)
library_tshwane.books.set([book1, book3])
library_mamelodi.books.set([book2, book3])
print(f"Tshwane Library books added: {library_tshwane.books.count()}")
print(f"Mamelodi Library books added: {library_mamelodi.books.count()}")

# Create Librarians 
librarian_tshwane, created = Librarian.objects.get_or_create(name="Ayanda Dlodlo", library=library_tshwane)
librarian_mamelodi, created = Librarian.objects.get_or_create(name="Tshepo Mchunu", library=library_mamelodi)
print(f"Librarian 1: {librarian_tshwane.name} for {library_tshwane.name}")
print(f"Librarian 2: {librarian_mamelodi.name} for {librarian_mamelodi.name}")

print("\n" + "=" * 50)
print("QUERY RESULTS")
print("=" * 50)

# Query books by a specific author (using a foreign key)
print("\n--- 1. Query all books by Jane Austen (Author) ---")
austen_books = author1.books.all()
for book in austen_books:
    print(f" - {book.title}")
    
# List all books in a library (many-to-many)
print("\n --- 2. List all books in Tshwane Library (Library) ---")
tshwane_books = library_tshwane.books.all()
for book in tshwane_books:
    print(f" - {book.title} (by {book.author.name})")
    
# Retrieve the librarian for a library (one-to-one relationship)
print(f"\n --- 3. Retrieve the Librarian for Mamelodi Library (Librarian) ---")
mams_librarian = library_tshwane.librarian
print(f" - Librarian: {mams_librarian.name}")

print("\n--- End of Script ---")

# Library.objects.get(name=library_name)