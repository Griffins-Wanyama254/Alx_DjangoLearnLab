from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer

# ---------------------------
# LIST ALL BOOKS
# ---------------------------
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Anyone can read

# ---------------------------
# RETRIEVE SINGLE BOOK
# ---------------------------
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Anyone can read

# ---------------------------
# CREATE A BOOK
# ---------------------------
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated

# ---------------------------
# UPDATE A BOOK
# ---------------------------
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated

# ---------------------------
# DELETE A BOOK
# ---------------------------
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated
