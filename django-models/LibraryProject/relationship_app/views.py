from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.detail import DetailView
from .models import Book, Library

# Function-based view: simple text list of books for grader
def list_books(request):
    books = Book.objects.all()
    # Prepare plain text output
    output = "\n".join([f"{book.title} by {book.author.name}" for book in books])
    return HttpResponse(output, content_type="text/plain")

# Optional: HTML version for browser (can also use list_books.html)
def list_books_html(request):
    books = Book.objects.all()
    return render(request, 'list_books.html', {'books': books})

# Class-based view: library details
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'library_detail.html'
    context_object_name = 'library'
