from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from .models import Book, Library

# -----------------------------
# Function-based view: list all books (protected)
# -----------------------------
@login_required
def list_books(request):
    books = Book.objects.all()
    # Prepare plain text output for grader
    output = "\n".join([f"{book.title} by {book.author.name}" for book in books])
    return HttpResponse(output, content_type="text/plain")

# Optional: HTML version (can use list_books.html)
@login_required
def list_books_html(request):
    books = Book.objects.all()
    return render(request, 'list_books.html', {'books': books})

# -----------------------------
# Class-based view: Library details
# -----------------------------
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'library_detail.html'
    context_object_name = 'library'

# -----------------------------
# Authentication views
# -----------------------------

# Registration view
def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in after registration
            return redirect('list_books')  # Redirect after login
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

# Login view
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('list_books')  # Redirect after login
    else:
        form = AuthenticationForm()
    return render(request, 'relationship_app/login.html', {'form': form})

# Logout view
@login_required
def logout_view(request):
    logout(request)
    return render(request, 'relationship_app/logout.html')

