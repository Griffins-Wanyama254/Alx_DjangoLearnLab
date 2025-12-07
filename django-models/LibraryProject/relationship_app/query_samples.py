from .models import Author, Book, Library, Librarian


#Query all books by a specific author

# Option 1: Using Author instance
author = Author.objects.get(name=author_name)
books_by_author = author.books.all()  # thanks to related_name='books'

# Option 2: Using Book filter directly
books_by_author = Book.objects.filter(author=author)

# Print results
for book in books_by_author:
    print(book.title)


#List all books in a library
library = Library.objects.get(name=library_name)
books_in_library = library.books.all()  # ManyToManyField reverse

for book in books_in_library:
    print(book.title)


#Retrieve the librarian for a library
library = Library.objects.get(name="Central Library")
librarian = library.librarian  # thanks to related_name='librarian'
librarian_name = Librarian.objects.get(library=library)
print(librarian.name)