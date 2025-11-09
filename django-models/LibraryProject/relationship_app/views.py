from django.shortcuts import render
from .models import Book

# Function-based view
def list_books(request):
    books = Book.objects.all()  # Fetch all books
    return render(request, 'list_books.html', {'books': books})


from django.views.generic.detail import DetailView
from .models import Library

# Class-based view
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'library_detail.html'
    context_object_name = 'library'
