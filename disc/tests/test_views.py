from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from disc.models import Disc, Manufacturer

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
        form_data = {
            "status": "lost",
            "color": "Blue",
            "notes": "Lost at the park",
            "latitude": 34.89495,
            "longitude": -86.44408,
        }
        response = self.client.post(reverse("submit_disc"), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Disc entry submitted successfully!")

        # Verify that the disc was saved with the correct user
        disc = Disc.objects.get()
        self.assertEqual(disc.user, self.user)
        self.assertEqual(disc.color, "Blue")

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
