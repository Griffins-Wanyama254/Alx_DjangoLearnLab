from rest_framework import generics, viewsets, permissions
from .models import Book
from .serializers import BookSerializer

# ListAPIView (optional)
class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # restrict access

# BookViewSet with full CRUD and permissions
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # only logged-in users can access
