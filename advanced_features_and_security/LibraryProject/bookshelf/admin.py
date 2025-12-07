from django.contrib import admin
from .models import Book
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.contrib.auth.models import Group, Permission
from .models import CustomUser  # your custom user model

# Register your models here.
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    search_fields = ('title', 'author')
    list_filter = ['publication_year']




class CustomUserChangeForm(forms.ModelForm):
    """Form for editing users in the admin."""
    class Meta:
        model = CustomUser
        fields = '__all__'


class CustomUserCreationForm(forms.ModelForm):
    """Form for creating users in the admin."""
    class Meta:
        model = CustomUser
        fields = ('email',)



class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = (
        "user_id",
        "username",
        "email",
        "is_staff",
        "is_active",
    )

    list_filter = ("is_staff", "is_active")

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal Info", {"fields": ("email",)}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
        ("Identifiers", {"fields": ("user_id",)}),  # Your custom field
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2", "is_staff", "is_active"),
            },
        ),
    )

    search_fields = ("email", "username")
    ordering = ("email",)


def create_groups():
    permissions = {
        "viewers": ["can_view"],
        "editors": ["can_view", "can_create", "can_edit"],
        "admins": ["can_view", "can_create", "can_edit", "can_delete"],
    }

    for group_name, perms in permissions.items():
        group, created = Group.objects.get_or_create(name=group_name.capitalize())

        for perm in perms:
            permission = Permission.objects.get(codename=perm)
            group.permissions.add(permission)

    print("Groups and permissions created successfully!")



admin.site.register(CustomUser, CustomUserAdmin)