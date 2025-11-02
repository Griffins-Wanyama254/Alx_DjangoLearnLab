# CRUD Operations in Django Shell

# CREATE

```python
from bookshelf.models import Book

book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
# Output: <Book: Book object (1)>

# RETRIEVE
from bookshelf.models import Book

Book.objects.all()
# Output: <QuerySet [<Book: 1984 by George Orwell (1949)>]>

# UPDATE
from bookshelf.models import Book

book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()

Book.objects.all()
# Output: <QuerySet [<Book: Nineteen Eighty-Four by George Orwell (1949)>]>

# DELETE
from bookshelf.models import Book

book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
# Output: (1, {'bookshelf.Book': 1})

Book.objects.all()
# Output: <QuerySet []>
