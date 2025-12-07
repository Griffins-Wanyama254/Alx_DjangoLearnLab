from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length = 200)
    author = models.CharField(max_length = 100)
    publication_year = models.IntegerField()
    content = models.TextField()

    class Meta:
        permissions = [
            ("can_view", "Can view articles"),
            ("can_create", "Can create articles"),
            ("can_edit", "Can edit articles"),
            ("can_delete", "Can delete articles"),
        ]

    def __str__(self):
        return self.title

class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

class CustomUserManager(BaseUserManager):
    """Manager for custom user model."""

    def create_user(self, email, password=None, **extra_fields):
        """Create and return a regular user."""
        if not email:
            raise ValueError("Users must have an email address")

        # Normalize email to avoid duplicates
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # encrypt the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser."""
        # Force admin permissions
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        # protections (VERY IMPORTANT)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)