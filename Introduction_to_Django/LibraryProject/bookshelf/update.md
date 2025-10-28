```markdown
### Update Operation

**Command:**
```python
# Update the title of the retrieved book and save the changes
retrieved_book.title = "Nineteen Eighty-Four"
retrieved_book.save()
# Verify the update by retrieving the object again or simply printing the saved object
print(retrieved_book.title)

# Expected output

# Nineteen Eighty-Four