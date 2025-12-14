from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    ProfileView,
    FollowUser,
    UnfollowUser
)

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('profile', ProfileView.as_view()),
    path('follow/<int:user_id>/', FollowUser.as_view()),
    path('unfollow/<int:user_id>/', UnfollowUser.as_view()),
]
