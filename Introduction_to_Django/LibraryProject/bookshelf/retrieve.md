```markdown
### Retrieve Operation

**Command:**
```python
# Retrieve the book instance we just created using its primary key (pk)
retrieved_book = Book.objects.get(pk=book.pk)
# Display all attributes
print(f"Title: {retrieved_book.title}")
print(f"Author: {retrieved_book.author}")
print(f"Publication Year: {retrieved_book.publication_year}")

# Expected output

# Title: 1984
# Author: George Orwell
# Publication Year: 1949