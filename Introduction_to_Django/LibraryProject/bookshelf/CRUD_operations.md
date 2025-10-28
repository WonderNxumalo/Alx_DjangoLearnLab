### `CRUD_operations.md`

```markdown
# Detailed CRUD Operations in Django Shell

This document captures the Python commands and their output from the `python manage.py shell` session for the `Book` model in the `bookshelf` app.

## 1. Create Operation

```python
>>> from bookshelf.models import Book
>>> book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
>>> book
<Book: 1984 by George Orwell (1949)>

## 2. Retrieve Operation

>>> retrieved_book = Book.objects.get(title="1984")
>>> retrieved_book
<Book: 1984 by George Orwell (1949)>
>>> retrieved_book.title
'1984'
>>> retrieved_book.author
'George Orwell'
>>> retrieved_book.publication_year
1949

# 3. Update Operation

>>> retrieved_book.title = "Nineteen Eighty-Four"
>>> retrieved_book.save()
>>> retrieved_book
<Book: Nineteen Eighty-Four by George Orwell (1949)>
>>> Book.objects.get(pk=retrieved_book.pk).title
'Nineteen Eighty-Four'

# 4. Delete Operation

>>> retrieved_book.delete()
(1, {'bookshelf.Book': 1})
>>> Book.objects.all()
<QuerySet []>