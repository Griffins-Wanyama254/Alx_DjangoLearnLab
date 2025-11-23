from django.urls import path
from .views import BookList

app_name = 'api'

urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),
]
