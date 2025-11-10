# from bookshelf.models import Book

```markdown
### Delete Operation

**Command:**
```python
# Delete the book instance
retrieved_book.delete()
# Confirm deletion by trying to retrieve all books.
# This should return an empty QuerySet if only one book existed.
Book.objects.all()

# Expected output

# (1, {'bookshelf.Book': 1})
# <QuerySet []>