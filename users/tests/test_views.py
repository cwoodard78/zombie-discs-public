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
        """Test that unauthenticated users are redirected to login when accessing a protected view."""
        protected_url = reverse('user_disc_list')  # Replace with an actual protected view name
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

    def test_public_profile_details(self):
        """Test that only public details are displayed on another user's profile."""
        response = self.client.get(reverse('profile', kwargs={'username': self.user2.username}))
        self.assertContains(response, self.user2.first_name)
        self.assertContains(response, self.user2.last_name)
        self.assertNotContains(response, self.user2.email)

    def test_nonexistent_profile(self):
        """Test that accessing a non-existent profile returns a 404 error."""
        response = self.client.get(reverse('profile', kwargs={'username': 'nonexistentuser'}))
        self.assertEqual(response.status_code, 404)

    def test_redirect_if_not_logged_in(self):
        """Test that unauthenticated users are redirected to login page when accessing a profile."""
        self.client.logout()
        response = self.client.get(reverse('profile', kwargs={'username': self.user1.username}))
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('profile', kwargs={'username': self.user1.username})}"
        )

    def test_case_sensitivity_in_usernames(self):
        """Test behavior for case variations in usernames."""
        response_lowercase = self.client.get(reverse('profile', kwargs={'username': 'testuser1'}))
        response_uppercase = self.client.get(reverse('profile', kwargs={'username': 'TestUser1'}))
        self.assertEqual(response_lowercase.status_code, 200)
        self.assertEqual(response_uppercase.status_code, 404)  # Assuming case sensitivity in your setup
class DeleteAccountTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123'
        )
        self.client.login(username='testuser', password='password123')

    def test_delete_account_view_get(self):
        """Test that the delete account view loads successfully"""
        response = self.client.get(reverse('delete_account'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Are you sure you want to delete your account?")

    def test_delete_account_view_post(self):
        """Test that the account is deleted on POST"""
        response = self.client.post(reverse('delete_account'))
        self.assertRedirects(response, reverse('home'))  # Assuming 'home' is your homepage
        self.assertFalse(User.objects.filter(username='testuser').exists())

class PasswordChangeTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='OldPassword123!'
        )
        self.client.login(username='testuser', password='OldPassword123!')

    def test_password_change_view(self):
        """Test that the password change view loads successfully"""
        response = self.client.get(reverse('password_change'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Change Password')

    def test_password_change_success(self):
        """Test that the password is successfully changed"""
        response = self.client.post(reverse('password_change'), {
            'old_password': 'OldPassword123!',
            'new_password1': 'NewStrongPassword123!',
            'new_password2': 'NewStrongPassword123!',
        })
        self.assertRedirects(response, reverse('password_change_done'))
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('NewStrongPassword123!'))

class AboutPageTests(TestCase):
    def setUp(self):
        self.url = reverse('about')

    def test_about_page_status_code(self):
        """Test that the About page loads successfully."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_about_page_template_used(self):
        """Test that the correct template is used for the About page."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'about.html')

    def test_about_page_content(self):
        """Test that the About page contains specific content."""
        response = self.client.get(self.url)
        self.assertContains(response, 'About Zombie Discs')  
        self.assertContains(response, 'Welcome to <strong>Zombie Discs</strong>')
