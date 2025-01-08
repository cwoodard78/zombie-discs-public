from django.test import TestCase
from django.urls import reverse

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