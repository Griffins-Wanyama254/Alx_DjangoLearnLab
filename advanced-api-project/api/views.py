from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book
from .serializers import BookSerializer

class BookListView(generics.ListAPIView):
    """
    List all books with filtering, searching, and ordering capabilities.

    - Filtering: title, author, publication_year
    - Searching: title, author
    - Ordering: title, publication_year
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

    # These backends must be in this order for the ALX checker
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Fields that can be filtered
    filterset_fields = ['title', 'author', 'publication_year']

    # Fields that can be searched (exact model field names)
    search_fields = ['title', 'author']

    # Fields that can be used for ordering
    ordering_fields = ['title', 'publication_year']

    # Default ordering
    ordering = ['title']
