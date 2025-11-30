from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer
from django.utils import timezone


# ---------------------------
# LIST ALL BOOKS
# ---------------------------
class BookListView(generics.ListAPIView):
    """
    Returns a list of all books.
    Unauthenticated users can access this (read-only).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


# ---------------------------
# RETRIEVE SINGLE BOOK BY ID
# ---------------------------
class BookDetailView(generics.RetrieveAPIView):
    """
    Retrieves a single book by its ID.
    Allows read-only access to unauthenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


# ---------------------------
# CREATE A NEW BOOK
# ---------------------------
class BookCreateView(generics.CreateAPIView):
    """
    Creates a new book.
    Only authenticated users can create.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Custom behavior (example):
        Ensure publication year is not in the future.
        """
        year = serializer.validated_data.get("publication_year")

        if year > timezone.now().year:
            raise ValueError("Publication year cannot be in the future.")

        serializer.save()


# ---------------------------
# UPDATE AN EXISTING BOOK
# ---------------------------
class BookUpdateView(generics.UpdateAPIView):
    """
    Updates an existing book.
    Only authenticated users can update books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        """
        Custom behavior:
        Additional validation during update.
        """
        year = serializer.validated_data.get("publication_year")

        if year > timezone.now().year:
            raise ValueError("Publication year cannot be in the future.")

        serializer.save()


# ---------------------------
# DELETE A BOOK
# ---------------------------
class BookDeleteView(generics.DestroyAPIView):
    """
    Deletes a book.
    Only authenticated users can delete.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
