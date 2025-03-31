from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from disc.models import Disc, Manufacturer

class DiscTemplateTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

        Disc.objects.create(
            user=self.user,
            status='lost',
            color='Yellow',
            notes='Near hole 7.',
            latitude=34.89495,
            longitude=-86.44408,
        )
        self.url = reverse('user_disc_list')

    def test_submit_disc_template_content(self):
        """Test that the submit_disc template renders correctly."""
        response = self.client.get(reverse('submit_disc'))
        self.assertContains(response, "Submit a Disc")
        self.assertContains(response, "Status")
        self.assertContains(response, "Color")
        self.assertContains(response, "Type")
        self.assertContains(response, "Manufacturer")
        self.assertContains(response, "Mold")
        self.assertContains(response, "Notes")
        self.assertContains(response, "Image")
        self.assertContains(response, "Optional Reward")

    def test_user_disc_list_template_content(self):
        """Test that the user_disc_list template displays discs correctly."""
        response = self.client.get(self.url)

        # Ensure the page loads successfully
        self.assertEqual(response.status_code, 200)

        # Check if the content of the disc is rendered properly
        self.assertContains(response, "Yellow")  # Status and color
        self.assertContains(response, "34.89495")
        self.assertContains(response, "-86.44408")

class DiscDetailTemplateTest(TestCase):
    def setUp(self):
        """Set up a user, a disc, and related data."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.manufacturer = Manufacturer.objects.create(name="Innova")
        self.disc = Disc.objects.create(
            user=self.user,
            status="Lost",
            color="Red",
            type="Driver",
            manufacturer=self.manufacturer,
            mold_name="Destroyer",
            notes="Left near the basket.",
            latitude=34.89495,
            longitude=-86.44408,
        )
        self.detail_url = reverse("disc_detail", args=[self.disc.id])

        # Log in the test user
        self.client.login(username="testuser", password="testpass")

    def test_disc_detail_from_user_disc_list(self):
        """Test that the 'Go to My Disc List' link appears when navigated from the user_disc_list."""
        response = self.client.get(f"{self.detail_url}?from_user_disc_list=true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Go to My Disc List")
        self.assertNotContains(response, "Add Another Disc")

class DiscMapTemplateTests(TestCase):
    def test_map_view_contains_map_div(self):
        """Test that the map view contains the required map div."""
        response = self.client.get(reverse('disc_map_view'))
        self.assertContains(response, '<div id="map"')

    def test_map_view_contains_toggle_buttons(self):
        """Test that the map view contains toggle buttons."""
        response = self.client.get(reverse('disc_map_view'))
        self.assertContains(response, 'id="showAll"')
        self.assertContains(response, 'id="showLost"')
        self.assertContains(response, 'id="showFound"')
