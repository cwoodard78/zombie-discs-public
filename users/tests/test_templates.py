from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class RegistrationTemplateTests(TestCase):

    def setUp(self):
        self.register_url = reverse('register')

    def test_registration_template_rendering(self):
        """Test that the registration template contains the correct elements"""
        response = self.client.get(self.register_url)
        self.assertContains(response, '<form')  # Form tag
        self.assertContains(response, 'name="username"')  # Username field
        self.assertContains(response, 'name="first_name"')  # First name field
        self.assertContains(response, 'name="last_name"')  # Last name field
        self.assertContains(response, 'name="email"')  # Email field
        self.assertContains(response, 'name="password"')  # Password field
        self.assertContains(response, 'csrfmiddlewaretoken')  # CSRF token

class LoginTemplateTests(TestCase):
    
    def setUp(self):
        self.login_url = reverse('login')

    def test_login_template_contains_form(self):
        """Test that the login template contains the form fields"""
        response = self.client.get(self.login_url)
        self.assertContains(response, 'name="username"')
        self.assertContains(response, 'name="password"')
        self.assertContains(response, 'csrfmiddlewaretoken')  # CSRF token for security

class ProfileTemplateTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            first_name='John',
            last_name='Doe',
            password='StrongPassword123!'
        )
        self.client.login(username='testuser', password='StrongPassword123!')

    def test_profile_template_content(self):
        """Test that the profile template displays user details"""
        response = self.client.get(reverse('profile', kwargs={'username': self.user.username}))  # Pass username
        self.assertContains(response, self.user.username)
        self.assertContains(response, self.user.email)
        self.assertContains(response, 'Edit Profile')

    def test_edit_profile_template_content(self):
        """Test that the edit profile template contains the form"""
        response = self.client.get(reverse('edit_profile'))
        self.assertContains(response, '<form')
        self.assertContains(response, 'Save Changes')
        self.assertContains(response, self.user.email)