from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from .models import Book
from .forms import ExampleForm

# Create your views here.

# VIEW LIST
@permission_required('yourapp.can_view', raise_exception=True)
def article_list(request):
    books = Book.objects.all()
    return render(request, "articles/list.html", {"articles": books})


# CREATE
@permission_required('yourapp.can_create', raise_exception=True)
def create_article(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        Book.objects.create(title=title, content=content)
        return redirect("article_list")

    return render(request, "articles/create.html")


# EDIT
@permission_required('yourapp.can_edit', raise_exception=True)
def edit_article(request, book_id):
    books = get_object_or_404(Book, id=book_id)

    if request.method == "POST":
        Book.title = request.POST.get("title")
        Book.content = request.POST.get("content")
        Book.save()
        return redirect("book_list")

    return render(request, "articles/edit.html", {"book": books})


# DELETE
@permission_required('yourapp.can_delete', raise_exception=True)
def delete_article(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return redirect("book_list")


# bookshelf/views.py
def create_book(request):
    if request.method == "POST":
        form = ExampleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = ExampleForm()
    return render(request, 'bookshelf/create.html', {'form': form})