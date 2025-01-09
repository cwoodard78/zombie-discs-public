from django.test import SimpleTestCase
from users.views import register
from django.urls import reverse, resolve
from django.contrib.auth.views import LoginView, LogoutView
from users.views import profile, edit_profile

class RegistrationURLTests(SimpleTestCase):

    def test_registration_url_resolves(self):
        """Test that the registration URL resolves to the correct view"""
        url = reverse('register')
        self.assertEqual(resolve(url).func, register)

class LoginURLTests(SimpleTestCase):

    def test_login_url_resolves(self):
        """Test that the login URL resolves to the Django LoginView"""
        url = reverse('login')
        self.assertEqual(resolve(url).func.view_class, LoginView)

class LogoutURLTests(SimpleTestCase):

    def test_logout_url_resolves(self):
        """Test that the logout URL resolves to the Django LogoutView"""
        url = reverse('logout')
        self.assertEqual(resolve(url).func.view_class, LogoutView)

class ProfileURLTests(SimpleTestCase):

    def test_profile_url_resolves(self):
        """Test that the profile URL resolves to the correct view"""
        url = reverse('profile', kwargs={'username': 'testuser'})
        self.assertEqual(resolve(url).func, profile)

    def test_edit_profile_url_resolves(self):
        """Test that the edit profile URL resolves to the correct view"""
        url = reverse('edit_profile')
        self.assertEqual(resolve(url).func, edit_profile)