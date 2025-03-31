"""
URL Configuration for the 'users' app.

Includes routes for:
- Authentication (register, login, logout)
- Profile management
- Karma system
- Password management (reset/change)
- Help page (FAQ)
- User API endpoint
"""

from django.urls import path
from django.contrib.auth.views import (
    LoginView, 
    LogoutView, 
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView, 
    PasswordResetCompleteView, 
    PasswordChangeView, 
    PasswordChangeDoneView
)

from . import views
from .views import (
    register,
    profile,
    edit_profile,
    delete_account, 
    award_karma, 
    help_view, 
    UserListAPIView
)

urlpatterns = [
    # AUTHENICATION
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # PROFILE MANAGEMENT
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('profile/<str:username>/', profile, name='profile'),
    path('delete_account/', delete_account, name='delete_account'),
    # KARMA SYSTEM
    path('karma/<str:username>/', award_karma, name='award_karma'),
    # HELP
    path("faq/", help_view, name="faq"),

    # Django password reset
    path('password_reset/', PasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'),
    path('password_reset_done/', PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset_done/', PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),

    # Password change from profile
    path('password_change/', PasswordChangeView.as_view(template_name='users/password_change.html'), name='password_change'),
    path('password_change_done/', PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'), name='password_change_done'),

    # API to List All Users
    path('', UserListAPIView.as_view(), name='user_list_api'),

]
