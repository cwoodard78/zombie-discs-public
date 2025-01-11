from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from disc.models import Disc, Manufacturer
from django.core.files.uploadedfile import SimpleUploadedFile

class DiscViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.manufacturer = Manufacturer.objects.create(name="Innova")
        self.client.login(username='testuser', password='testpass')

    def test_submit_disc_view_get(self):
        """Test that the submit_disc view loads correctly."""
        response = self.client.get(reverse('submit_disc'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Submit a Disc")
        self.assertTemplateUsed(response, "disc/submit_disc.html")

    def test_submit_disc_view_post_valid(self):
        """Test that the submit_disc view creates a disc on valid POST."""
        form_data = {
            "status": "lost",
            "color": "Red",
            "latitude": 34.89,
            "longitude": -86.44,
            "notes": "Lost near the basket."
        }
        response = self.client.post(reverse('submit_disc'), data=form_data)

        # Check if the response redirects
        self.assertEqual(response.status_code, 302)

        # Verify the redirect location (e.g., to the disc details page)
        self.assertRedirects(response, reverse('disc_detail', args=[1]))

    def test_submit_disc_view_post_invalid(self):
        """Test that the submit_disc view returns errors on invalid POST."""
        form_data = {
            'status': 'lost',
            'color': '',
            'latitude': 34.89495,
            'longitude': -86.44408,
        }
        response = self.client.post(reverse('submit_disc'), data=form_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('errors', response.json())

    def test_user_disc_list_view(self):
        """Test that the user_disc_list view shows the user's discs."""
        Disc.objects.create(
            status='found',
            color='Green',
            notes='Found on hole 3.',
            latitude=34.89495,
            longitude=-86.44408,
            user=self.user,
        )
        response = self.client.get(reverse('user_disc_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Green")

    def test_disc_with_image_view(self):
        """Test that a disc with an image displays correctly."""
        image_file = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        disc = Disc.objects.create(
            status='lost',
            color='Red',
            notes='Lost near hole 7.',
            latitude=34.89495,
            longitude=-86.44408,
            user=self.user,
            manufacturer=self.manufacturer,
            mold_name='Destroyer',
            image=image_file
        )
        url = reverse('disc_detail', kwargs={'disc_id': disc.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, disc.image.url)

    def test_disc_without_image_view(self):
        """Test that a disc without an image displays correctly."""
        disc = Disc.objects.create(
            status='found',
            color='Blue',
            notes='Found near the basket.',
            latitude=34.89500,
            longitude=-86.44450,
            user=self.user,
            manufacturer=self.manufacturer,
            mold_name='Firebird'
        )
        url = reverse('disc_detail', kwargs={'disc_id': disc.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, '<img')
        
class ViewMyDiscsTests(TestCase):
    def setUp(self):
        # Create a user and log them in
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123'
        )
        self.client.login(username='testuser', password='password123')

        # Create another user
        self.other_user = User.objects.create_user(
            username='otheruser',
            email='otheruser@example.com',
            password='password123'
        )

        # Create discs for the authenticated user
        self.user_discs = [
            Disc.objects.create(
                user=self.user,
                status='Lost',
                color='Red',
                latitude=34.89,
                longitude=-86.44,
                notes='Lost near the basket.'
            ),
            Disc.objects.create(
                user=self.user,
                status='Lost',
                color='Blue',
                latitude=34.88,
                longitude=-86.43,
                notes='Found near the tee.'
            ),
        ]

        # Create discs for another user
        self.other_user_discs = [
            Disc.objects.create(
                user=self.other_user,
                status='Found',
                color='Yellow',
                latitude=34.87,
                longitude=-86.42,
                notes='Lost in the woods.'
            ),
        ]

        # Define the URL for "View My Discs"
        self.url = reverse('user_disc_list')  # Replace with your actual URL name for the view

    def test_user_disc_list_status_code(self):
        """Test that the View My Discs page loads successfully."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_user_disc_list_template_used(self):
        """Test that the correct template is used for the View My Discs page."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'disc/user_disc_list.html')  # Replace with the actual template name

    def test_user_disc_list_displays_correct_discs(self):
        """Test that the User Discs page displays only the discs for the authenticated user."""
        response = self.client.get(self.url)
        content = response.content.decode('utf-8')

        # Ensure discs for the authenticated user are displayed
        for disc in self.user_discs:
            self.assertContains(response, disc.color)
            self.assertContains(response, disc.status)

        # Ensure discs for other users are NOT displayed
        for disc in self.other_user_discs:
            self.assertNotContains(response, disc.color)
            self.assertNotContains(response, disc.status)

    def test_user_disc_list_correct_number_of_discs(self):
        """Test that the correct number of discs is displayed for the authenticated user."""
        response = self.client.get(self.url)
        discs_displayed = response.context['discs']  # Replace with the actual context variable name
        self.assertEqual(len(discs_displayed), len(self.user_discs))

class EditDiscTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.other_user = User.objects.create_user(username="otheruser", password="password")
        self.disc = Disc.objects.create(
            user=self.user,
            status="lost",
            color="Yellow",
            notes="Near the basket.",
            latitude=34.89495,
            longitude=-86.44408
        )

    def test_edit_disc_accessible_by_owner(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("edit_disc", args=[self.disc.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Disc")

    def test_edit_disc_not_accessible_by_other_user(self):
        self.client.login(username="otheruser", password="password")
        response = self.client.get(reverse("edit_disc", args=[self.disc.id]))
        self.assertEqual(response.status_code, 403)

    def test_edit_disc_updates_data(self):
        self.client.login(username="testuser", password="password")
        response = self.client.post(
            reverse("edit_disc", args=[self.disc.id]),
            {
                "status": "found",
                "color": "Blue",
                "latitude": 34.89495,
                "longitude": -86.44408,
                "notes": "Updated notes.",
            }
        )
        self.assertRedirects(response, reverse("disc_detail", args=[self.disc.id]))
        self.disc.refresh_from_db()
        self.assertEqual(self.disc.color, "Blue")
        self.assertEqual(self.disc.notes, "Updated notes.")

class DeleteDiscViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.other_user = User.objects.create_user(username='otheruser', password='password')
        self.disc = Disc.objects.create(
            user=self.user,
            status='lost',
            color='Yellow',
            notes='Near hole 7.',
            latitude=34.89495,
            longitude=-86.44408
        )
        self.url = reverse('delete_disc', kwargs={'disc_id': self.disc.id})

    def test_delete_disc_get(self):
        """Test that the delete confirmation page is accessible."""
        self.client.login(username='testuser', password='password')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Are you sure you want to delete this disc?")

    def test_delete_disc_post(self):
        """Test that the disc is deleted on POST."""
        self.client.login(username='testuser', password='password')
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('user_disc_list'))
        self.assertFalse(Disc.objects.filter(id=self.disc.id).exists())

    def test_delete_disc_unauthorized_user(self):
        """Test that an unauthorized user cannot delete the disc."""
        self.client.login(username='otheruser', password='password')
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('user_disc_list'))
        self.assertTrue(Disc.objects.filter(id=self.disc.id).exists())

    def test_delete_disc_not_logged_in(self):
        """Test that an unauthenticated user cannot access the delete page."""
        response = self.client.get(self.url)
        self.assertRedirects(response, f"{reverse('login')}?next={self.url}")