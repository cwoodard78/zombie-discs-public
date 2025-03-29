from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from .views import delete_account
from django.contrib.auth import views as auth_views

from rest_framework.generics import RetrieveAPIView
from .views import UserListAPIView
from .views import help_view

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('delete_account/', delete_account, name='delete_account'),
    path('karma/<str:username>/', views.award_karma, name='award_karma'),
    path("faq/", help_view, name="faq"),

    # Django password reset
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset_done/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),

    # Password change from profile
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='users/password_change.html'), name='password_change'),
    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'), name='password_change_done'),

    # API
    # path('api/users/', UserListAPIView.as_view(), name='user_list_api'),
    path('', UserListAPIView.as_view(), name='user_list_api'),

]
