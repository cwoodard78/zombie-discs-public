from django.test import TestCase
from users.forms import RegistrationForm, ProfileForm
from django.contrib.auth.models import User
from django.urls import reverse

VALID_USER_DATA = {
    'username': 'testuser',
    'first_name': 'John',
    'last_name': 'Doe',
    'email': 'testuser@example.com',
    'password': 'StrongPass123!',
}

"""REGISTRATION"""
class RegistrationFormTests(TestCase):

    def setUp(self):
        self.valid_data = VALID_USER_DATA.copy()


    def test_valid_form(self):
        """Ensure the form is valid with correct input"""
        form = RegistrationForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_missing_required_field(self):
        """Test that the form is invalid if a required field is missing"""
        data = self.valid_data.copy()
        data.pop('username')  # Remove the username field
        form = RegistrationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    def test_invalid_username(self):
        """Test that the form rejects an invalid username"""
        data = self.valid_data.copy()
        data['username'] = 'invalid!user'
        form = RegistrationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.', form.errors['username'])

    def test_invalid_email(self):
        """Test that the form rejects an invalid email"""
        data = self.valid_data.copy()
        data['email'] = 'invalid-email'
        form = RegistrationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('Enter a valid email address.', form.errors['email'])

class LoginFormTests(TestCase):

    def setUp(self):
        # Create a user to test login functionality
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='StrongPass123!'
        )
        self.login_url = reverse('login')

    # Form Tests
    def test_login_form_required_fields(self):
        """Test that both username and password are required for login"""
        response = self.client.post(self.login_url, data={'username': '', 'password': ''})
        self.assertEqual(response.status_code, 200)  # Form errors reload the page
        self.assertContains(response, 'This field is required.')

    def test_login_with_invalid_credentials(self):
        """Test that login fails with invalid credentials"""
        response = self.client.post(self.login_url, data={'username': 'wronguser', 'password': 'wrongpass'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please enter a correct username and password.')
        self.assertNotIn('_auth_user_id', self.client.session)  # User not authenticated

    def test_login_with_valid_credentials(self):
        """Test that login succeeds with valid credentials"""
        response = self.client.post(self.login_url, data={'username': 'testuser', 'password': 'StrongPass123!'})
        self.assertEqual(response.status_code, 302)  # Redirects after successful login
        self.assertIn('_auth_user_id', self.client.session)  # User is authenticated

class ProfileFormTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            first_name='John',
            last_name='Doe'
        )

    def test_valid_form(self):
        """Test that the form is valid with correct data"""
        form = ProfileForm(data={
            'email': 'newemail@example.com',
            'first_name': 'Jane',
            'last_name': 'Smith',
        }, instance=self.user)
        self.assertTrue(form.is_valid())

    def test_missing_required_field(self):
        """Test that the form is invalid if a required field is missing"""
        form = ProfileForm(data={
            'email': '',
            'first_name': 'Jane',
            'last_name': 'Smith',
        }, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_invalid_email(self):
        """Test that the form is invalid with an invalid email"""
        form = ProfileForm(data={
            'email': 'not-an-email',
            'first_name': 'Jane',
            'last_name': 'Smith',
        }, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)