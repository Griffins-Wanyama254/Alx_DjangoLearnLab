from django.urls import path
from .views import (
    home, register_view, login_view, logout_view, profile_view,
    PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView
)


urlpatterns = [
    # Post URLs
    path('', views.home, name='home'),
    path('posts/', views.PostListView.as_view(), name='post-list'),
    path('posts/new/', views.PostCreateView.as_view(), name='post-create'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post-update'),
    path('posts/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),

    # Comment URLs
    path('posts/<int:post_pk>/comments/new/', views.CommentCreateView.as_view(), name='comment-create'),
    path('comments/<int:pk>/edit/', views.CommentUpdateView.as_view(), name='comment-update'),
    path('comments/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment-delete'),

    # Auth URLs
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
]
