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

class ProfileViewTests(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            username='testuser1',
            email='testuser1@example.com',
            first_name='John',
            last_name='Doe',
            password='StrongPassword123!'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            email='testuser2@example.com',
            first_name='Jane',
            last_name='Smith',
            password='AnotherStrongPassword456!'
        )
        # Log in as user1
        self.client.login(username='testuser1', password='StrongPassword123!')
        # Edit profile URL
        self.edit_profile_url = reverse('edit_profile')

    def test_profile_view(self):
        """Test that the profile view loads successfully for an authenticated user"""
        response = self.client.get(reverse('profile', kwargs={'username': self.user1.username}))  # Pass username
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user1.username)
        self.assertContains(response, self.user1.email)

    def test_edit_profile_view_get(self):
        """Test that the edit profile view loads successfully with pre-filled form"""
        response = self.client.get(reverse('edit_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user1.username)
        self.assertContains(response, self.user1.email)
        self.assertContains(response, 'Save Changes')

    def test_edit_profile_view_post_valid_data(self):
        """Test that the edit profile view updates the user's data on valid POST"""
        response = self.client.post(reverse('edit_profile'), data={
            'email': 'newemail@example.com',
            'first_name': 'Jane',
            'last_name': 'Smith',
        })
        self.assertRedirects(response, reverse('profile', kwargs={'username': self.user1.username}))  # Pass username
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.email, 'newemail@example.com')
        self.assertEqual(self.user1.first_name, 'Jane')
        self.assertEqual(self.user1.last_name, 'Smith')

    def test_edit_profile_view_post_invalid_data(self):
        """Test that the edit profile view does not update data on invalid POST"""
        invalid_data = {
            'email': 'not-an-email',  # Invalid email
            'first_name': '',         # Missing first name
            'last_name': 'Smith',     # Valid last name
        }
        response = self.client.post(self.edit_profile_url, data=invalid_data)
        self.assertEqual(response.status_code, 200)  # Page reloads with errors
        self.assertContains(response, 'Enter a valid email address.')  # Check specific field error
        self.assertContains(response, 'This field is required.')       # Check missing field error

    def test_other_user_profile_no_edit_link(self):
        """Test that another user's profile does not have the 'Edit Profile' link"""
        response = self.client.get(reverse('profile', kwargs={'username': self.user2.username}))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Edit Profile')  # Ensure 'Edit Profile' link is not visible

    # def test_cannot_access_other_user_edit_profile(self):
    #     """Test that a user cannot access the edit profile page of another user"""
    #     # Ensure user1 cannot access the edit profile page for user2
    #     response = self.client.get(reverse('edit_profile'))
    #     self.assertEqual(response.status_code, 200)  # Own edit profile is accessible

    def test_cannot_access_other_user_edit_profile(self):
        """Test that a user cannot access the edit profile page of another user"""
        # Login as user2
        self.client.logout()
        self.client.login(username='testuser2', password='AnotherStrongPassword456!')
        
        # Ensure user2 can access their own edit profile page
        response = self.client.get(reverse('edit_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user2.username)  # Ensure user2 sees their username

        # Ensure user2 cannot tamper and access user1's profile edit page (unauthorized)
        self.client.logout()
        self.client.login(username='testuser1', password='StrongPassword123!')

        # Attempting to access edit profile URL should only affect their own profile
        response = self.client.get(reverse('edit_profile'))
        self.assertEqual(response.status_code, 200)  # User1 can access their own edit page
        self.assertContains(response, self.user1.username)  # Ensure user1 sees only their username
        self.assertNotContains(response, self.user2.username)  # Ensure user2's username is not displayed