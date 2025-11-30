from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Book, Author
from datetime import date


class BookAPITestCase(TestCase):
    """
    Comprehensive test suite for Book API endpoints.
    Tests CRUD operations, filtering, searching, ordering, and permissions.
    """

    def setUp(self):
        """
        Set up test data and client before each test method.
        This runs before every test.
        """
        # Create API client
        self.client = APIClient()
        
        # Create test users
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.admin_user = User.objects.create_superuser(
            username='admin',
            password='adminpass123'
        )
        
        # Create test authors
        self.author1 = Author.objects.create(name='J.K. Rowling')
        self.author2 = Author.objects.create(name='George Orwell')
        self.author3 = Author.objects.create(name='Jane Austen')
        
        # Create test books
        self.book1 = Book.objects.create(
            title='Harry Potter',
            publication_year=1997,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title='1984',
            publication_year=1949,
            author=self.author2
        )
        self.book3 = Book.objects.create(
            title='Pride and Prejudice',
            publication_year=1813,
            author=self.author3
        )
        
        # Define URLs (adjust these based on your urls.py)
        self.list_url = reverse('book-list')  # Adjust name as per your urls.py
        self.detail_url = lambda pk: reverse('book-detail', kwargs={'pk': pk})
        self.create_url = reverse('book-create')
        self.update_url = lambda pk: reverse('book-update', kwargs={'pk': pk})
        self.delete_url = lambda pk: reverse('book-delete', kwargs={'pk': pk})

    def tearDown(self):
        """
        Clean up after each test.
        """
        Book.objects.all().delete()
        Author.objects.all().delete()
        User.objects.all().delete()


    # ==================== LIST VIEW TESTS ====================
    
    def test_book_list_unauthenticated(self):
        """
        Test that unauthenticated users can view the book list.
        Permission: IsAuthenticatedOrReadOnly allows read access.
        """
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)  # Should return all 3 books
    
    def test_book_list_authenticated(self):
        """
        Test that authenticated users can view the book list.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
    
    def test_book_list_response_structure(self):
        """
        Test that the response contains the correct fields.
        """
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check first book structure
        book_data = response.data[0]
        self.assertIn('id', book_data)
        self.assertIn('title', book_data)
        self.assertIn('publication_year', book_data)
        self.assertIn('author', book_data)
        
        # Check author nested structure
        self.assertIn('id', book_data['author'])
        self.assertIn('name', book_data['author'])


    # ==================== DETAIL VIEW TESTS ====================
    
    def test_book_detail_success(self):
        """
        Test retrieving a single book by ID.
        """
        response = self.client.get(self.detail_url(self.book1.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Harry Potter')
        self.assertEqual(response.data['publication_year'], 1997)
        self.assertEqual(response.data['author']['name'], 'J.K. Rowling')
    
    def test_book_detail_not_found(self):
        """
        Test retrieving a non-existent book returns 404.
        """
        response = self.client.get(self.detail_url(9999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    # ==================== CREATE VIEW TESTS ====================
    
    def test_book_create_unauthenticated(self):
        """
        Test that unauthenticated users cannot create books.
        """
        data = {
            'title': 'New Book',
            'publication_year': 2020,
            'author_id': self.author1.id
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_book_create_authenticated_success(self):
        """
        Test that authenticated users can create books.
        """
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'The Hobbit',
            'publication_year': 1937,
            'author_id': self.author1.id
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)
        
        # Verify the created book
        new_book = Book.objects.get(title='The Hobbit')
        self.assertEqual(new_book.publication_year, 1937)
        self.assertEqual(new_book.author, self.author1)
    
    def test_book_create_future_year_validation(self):
        """
        Test that books with future publication years are rejected.
        """
        self.client.force_authenticate(user=self.user)
        future_year = date.today().year + 1
        data = {
            'title': 'Future Book',
            'publication_year': future_year,
            'author_id': self.author1.id
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)
    
    def test_book_create_missing_required_fields(self):
        """
        Test that creating a book without required fields fails.
        """
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'Incomplete Book'
            # Missing publication_year and author_id
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    # ==================== UPDATE VIEW TESTS ====================
    
    def test_book_update_authenticated_success(self):
        """
        Test that authenticated users can update books.
        """
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'Harry Potter Updated',
            'publication_year': 1998,
            'author_id': self.author1.id
        }
        response = self.client.put(
            self.update_url(self.book1.pk), 
            data, 
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify the update
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Harry Potter Updated')
        self.assertEqual(self.book1.publication_year, 1998)
    
    def test_book_partial_update(self):
        """
        Test partial update (PATCH) of a book.
        """
        self.client.force_authenticate(user=self.user)
        data = {'title': '1984 - Updated Edition'}
        response = self.client.patch(
            self.update_url(self.book2.pk), 
            data, 
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify only title changed
        self.book2.refresh_from_db()
        self.assertEqual(self.book2.title, '1984 - Updated Edition')
        self.assertEqual(self.book2.publication_year, 1949)  # Unchanged
    
    def test_book_update_unauthenticated(self):
        """
        Test that unauthenticated users cannot update books.
        """
        data = {
            'title': 'Unauthorized Update',
            'publication_year': 2000,
            'author_id': self.author1.id
        }
        response = self.client.put(
            self.update_url(self.book1.pk), 
            data, 
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    # ==================== DELETE VIEW TESTS ====================
    
    def test_book_delete_authenticated_success(self):
        """
        Test that authenticated users can delete books.
        """
        self.client.force_authenticate(user=self.user)
        initial_count = Book.objects.count()
        response = self.client.delete(self.delete_url(self.book1.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), initial_count - 1)
        
        # Verify book is actually deleted
        with self.assertRaises(Book.DoesNotExist):
            Book.objects.get(pk=self.book1.pk)
    
    def test_book_delete_unauthenticated(self):
        """
        Test that unauthenticated users cannot delete books.
        """
        response = self.client.delete(self.delete_url(self.book1.pk))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Book.objects.count(), 3)  # No deletion occurred


    # ==================== FILTERING TESTS ====================
    
    def test_filter_by_publication_year(self):
        """
        Test filtering books by publication year.
        """
        response = self.client.get(self.list_url, {'publication_year': 1949})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], '1984')
    
    def test_filter_by_author(self):
        """
        Test filtering books by author ID.
        """
        response = self.client.get(self.list_url, {'author': self.author2.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['author']['name'], 'George Orwell')


    # ==================== SEARCHING TESTS ====================
    
    def test_search_by_title(self):
        """
        Test searching books by title.
        """
        response = self.client.get(self.list_url, {'search': 'Harry'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
        self.assertIn('Harry', response.data[0]['title'])
    
    def test_search_by_author_name(self):
        """
        Test searching books by author name.
        """
        response = self.client.get(self.list_url, {'search': 'Orwell'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['author']['name'], 'George Orwell')
    
    def test_search_no_results(self):
        """
        Test search with no matching results.
        """
        response = self.client.get(self.list_url, {'search': 'NonexistentBook'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)


    # ==================== ORDERING TESTS ====================
    
    def test_ordering_by_title_ascending(self):
        """
        Test ordering books by title in ascending order.
        """
        response = self.client.get(self.list_url, {'ordering': 'title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles))
    
    def test_ordering_by_title_descending(self):
        """
        Test ordering books by title in descending order.
        """
        response = self.client.get(self.list_url, {'ordering': '-title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles, reverse=True))
    
    def test_ordering_by_publication_year(self):
        """
        Test ordering books by publication year.
        """
        response = self.client.get(self.list_url, {'ordering': 'publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, sorted(years))


    # ==================== COMBINED FUNCTIONALITY TESTS ====================
    
    def test_filter_search_and_order_combined(self):
        """
        Test combining filtering, searching, and ordering.
        """
        # Create more test data
        Book.objects.create(
            title='Harry Potter and the Chamber of Secrets',
            publication_year=1998,
            author=self.author1
        )
        
        response = self.client.get(
            self.list_url, 
            {
                'search': 'Harry',
                'ordering': 'publication_year'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
        
        # Verify results are ordered
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, sorted(years))


# ==================== ADDITIONAL TEST CASES ====================

class AuthorAPITestCase(TestCase):
    """
    Test cases for Author model if you have Author endpoints.
    """
    
    def setUp(self):
        self.client = APIClient()
        self.author = Author.objects.create(name='Test Author')
    
    def test_author_string_representation(self):
        """
        Test the string representation of Author model.
        """
        self.assertEqual(str(self.author), 'Test Author')


class BookModelTestCase(TestCase):
    """
    Test cases for Book model methods and properties.
    """
    
    def setUp(self):
        self.author = Author.objects.create(name='Test Author')
        self.book = Book.objects.create(
            title='Test Book',
            publication_year=2020,
            author=self.author
        )
    
    def test_book_string_representation(self):
        """
        Test the string representation of Book model.
        """
        self.assertEqual(str(self.book), 'Test Book')
    
    def test_book_author_relationship(self):
        """
        Test the foreign key relationship between Book and Author.
        """
        self.assertEqual(self.book.author, self.author)
        self.assertIn(self.book, self.author.book_set.all())