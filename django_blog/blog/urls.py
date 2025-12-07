from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),

    # Authentication
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),

    # Blog Posts CRUD
    path('posts/', views.PostListView.as_view(), name='post-list'),
    path('posts/new/', views.PostCreateView.as_view(), name='post-create'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post-update'),
    path('posts/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),

    # Comments CRUD (nested under posts)
    path('posts/<int:post_pk>/comments/new/', views.CommentCreateView.as_view(), name='comment-create'),
    path('posts/<int:post_pk>/comments/<int:pk>/edit/', views.CommentUpdateView.as_view(), name='comment-update'),
    path('posts/<int:post_pk>/comments/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment-delete'),

    # Tagging
    path('tags/<str:tag>/', views.posts_by_tag, name='posts-by-tag'),

    # Search
    path('search/', views.search_posts, name='search-posts'),
]
