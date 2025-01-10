from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from disc.models import Disc

class DiscTemplateTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_submit_disc_template_content(self):
        """Test that the submit_disc template renders correctly."""
        response = self.client.get(reverse('submit_disc'))
        self.assertContains(response, "Submit a Disc")
        self.assertContains(response, "Select Coordinates")

    def test_user_disc_list_template_content(self):
        """Test that the user_disc_list template displays discs correctly."""
        Disc.objects.create(
            status='lost',
            color='Yellow',
            notes='Near hole 7.',
            latitude=34.89495,
            longitude=-86.44408,
            user=self.user,
        )
        response = self.client.get(reverse('user_disc_list'))
        self.assertContains(response, "Yellow")
        self.assertContains(response, "Near hole 7.")
