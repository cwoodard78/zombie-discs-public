from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

VALID_USER_DATA = {
    'username': 'testuser',
    'first_name': 'John',
    'last_name': 'Doe',
    'email': 'testuser@example.com',
    'password': 'StrongPass123!',
}

class RegistrationPageTests(TestCase):

    def setUp(self):
        self.register_url = reverse('register')
        self.valid_data = VALID_USER_DATA.copy()

    def test_registration_page_loads(self):
        """Test that the registration page loads successfully"""
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Register')  # Is 'Register' on the page?

    def test_registration_with_valid_data(self):
        """Test that a user can register with valid data"""
        response = self.client.post(self.register_url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)  # Good redirect after successful registration
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_registration_with_missing_username(self):
        """Test that registration fails if the username is missing"""
        data = self.valid_data.copy()
        data.pop('username')  # Remove the username field
        response = self.client.post(self.register_url, data=data)
        self.assertEqual(response.status_code, 200)  # Page reloads with error
        self.assertContains(response, 'This field is required.')
        self.assertFalse(User.objects.filter(email='testuser@example.com').exists())

    def test_registration_with_invalid_email(self):
        """Test that registration fails with an invalid email"""
        data = self.valid_data.copy()
        data['email'] = 'invalid-email'  # Invalid email format
        response = self.client.post(self.register_url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Enter a valid email address.')
        self.assertFalse(User.objects.filter(username='testuser').exists())

    def test_registration_with_weak_password(self):
        """Test that registration fails with a weak password"""
        data = self.valid_data.copy()
        data['password'] = '12345'  # Weak password
        response = self.client.post(self.register_url, data=data)
        self.assertEqual(response.status_code, 200)  # Page reloads with error
        self.assertContains(response, "This password is too short.")  # Default error from MinimumLengthValidator
        self.assertFalse(User.objects.filter(username='testuser').exists())

    def test_registration_with_weak_password(self):
        """Test that registration fails with a strong, too short password"""
        data = self.valid_data.copy()
        data['password'] = 'z%h(k1@'  # Weak password
        response = self.client.post(self.register_url, data=data)
        self.assertEqual(response.status_code, 200)  # Page reloads with error
        self.assertContains(response, "This password is too short.")  # Default error from MinimumLengthValidator
        self.assertFalse(User.objects.filter(username='testuser').exists())

    def test_registration_with_malicious_input(self):
        """Test that registration prevents SQL injection or malicious inputs"""
        data = self.valid_data.copy()
        data['username'] = "testuser'); DROP TABLE users; --"
        response = self.client.post(self.register_url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="testuser'); DROP TABLE users; --").exists())

    def test_registration_with_no_data(self):
        """Test that registration fails if no data is provided"""
        response = self.client.post(self.register_url, data={})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required.')
        self.assertFalse(User.objects.exists())

class RegistrationViewTests(TestCase):

    def setUp(self):
        self.register_url = reverse('register')
        self.valid_data = VALID_USER_DATA.copy()

    def test_get_registration_page(self):
        """Test that the registration page loads successfully"""
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Register')  # Check if the page contains 'Register'

    def test_post_valid_registration(self):
        """Test that a valid form submission creates a new user"""
        response = self.client.post(self.register_url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)  # Redirects on success
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_post_invalid_registration(self):
        """Test that an invalid form submission reloads the page with errors"""
        data = self.valid_data.copy()
        data['email'] = 'invalid-email'
        response = self.client.post(self.register_url, data=data)
        self.assertEqual(response.status_code, 200)  # Page reloads with errors
        self.assertContains(response, 'Enter a valid email address.')
        self.assertFalse(User.objects.filter(username='testuser').exists())

class LoginViewTests(TestCase):

    def setUp(self):
        # Create a user to test login functionality
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='StrongPass123!'
        )
        self.login_url = reverse('login')

    def test_login_page_renders_correctly(self):
        """Test that the login page loads successfully"""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Login')  # Ensure 'Login' appears in the page

    def test_redirect_after_login(self):
        """Test that a successful login redirects to LOGIN_REDIRECT_URL"""
        response = self.client.post(self.login_url, data={'username': 'testuser', 'password': 'StrongPass123!'})
        self.assertRedirects(response, '/')  # Match LOGIN_REDIRECT_URL from settings.py

    def test_protected_view_redirects_unauthenticated_users(self):
        """Test that unauthenticated users are redirected to login when accessing a protected view"""
        protected_url = reverse('protected_view')  # Replace with your actual protected view URL name
        response = self.client.get(protected_url)
        self.assertRedirects(response, f"{self.login_url}?next={protected_url}")  # Redirect with `next` parameter