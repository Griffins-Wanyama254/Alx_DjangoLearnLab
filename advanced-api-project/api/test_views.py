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
        self.list_url = reverse('book-list')
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


    # ==================== LOGIN TESTS ====================
    
    def test_user_login_success(self):
        """
        Test successful user login using client.login()
        """
        login_successful = self.client.login(
            username='testuser',
            password='testpass123'
        )
        self.assertTrue(login_successful)
    
    def test_user_login_failure(self):
        """
        Test failed login with incorrect credentials using client.login()
        """
        login_successful = self.client.login(
            username='testuser',
            password='wrongpassword'
        )
        self.assertFalse(login_successful)
    
    def test_book_create_with_login(self):
        """
        Test creating a book after logging in using client.login()
        """
        # Login first
        self.client.login(username='testuser', password='testpass123')
        
        data = {
            'title': 'The Hobbit',
            'publication_year': 1937,
            'author_id': self.author1.id
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)
    
    def test_book_update_with_login(self):
        """
        Test updating a book after logging in using client.login()
        """
        # Login first
        self.client.login(username='testuser', password='testpass123')
        
        data = {
            'title': 'Harry Potter - Updated',
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
        self.assertEqual(self.book1.title, 'Harry Potter - Updated')
    
    def test_book_delete_with_login(self):
        """
        Test deleting a book after logging in using client.login()
        """
        # Login first
        self.client.login(username='testuser', password='testpass123')
        
        initial_count = Book.objects.count()
        response = self.client.delete(self.delete_url(self.book1.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), initial_count - 1)
    
    def test_admin_login_and_access(self):
        """
        Test admin user login and access using client.login()
        """
        # Login as admin
        login_successful = self.client.login(
            username='admin',
            password='adminpass123'
        )
        self.assertTrue(login_successful)
        
        # Admin should be able to create books
        data = {
            'title': 'Admin Created Book',
            'publication_year': 2021,
            'author_id': self.author1.id
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_logout_after_login(self):
        """
        Test that logout works after login using client.login()
        """
        # Login first
        self.client.login(username='testuser', password='testpass123')
        
        # Verify user can create while logged in
        data = {
            'title': 'Logged In Book',
            'publication_year': 2020,
            'author_id': self.author1.id
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Logout
        self.client.logout()
        
        # Try to create again after logout - should fail
        data2 = {
            'title': 'Logged Out Book',
            'publication_year': 2021,
            'author_id': self.author1.id
        }
        response = self.client.post(self.create_url, data2, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    # ==================== LIST VIEW TESTS ====================
    
    def test_book_list_unauthenticated(self):
        """
        Test that unauthenticated users can view the book list.
        Permission: IsAuthenticatedOrReadOnly allows read access.
        """
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
    
    def test_book_list_authenticated(self):
        """
        Test that authenticated users can view the book list.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
    
    def test_book_list_with_login(self):
        """
        Test book list access after login using client.login()
        """