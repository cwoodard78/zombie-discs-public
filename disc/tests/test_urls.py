from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve
from disc.views import submit_disc, map_view, edit_disc
from disc.views import disc_map_view, DiscMapAPIView

class DiscURLSimpleTests(SimpleTestCase):
    """Tests for URL resolution that do not require database access."""

    def test_submit_disc_url_resolves(self):
        """Test that the submit_disc URL resolves correctly."""
        url = reverse('submit_disc')
        self.assertEqual(resolve(url).func, submit_disc)

    def test_map_view_url_resolves(self):
        """Test that the map_view URL resolves correctly."""
        url = reverse('map_view')
        self.assertEqual(resolve(url).func, map_view)

class DiscURLDatabaseTests(TestCase):
    """Tests for URLs that interact with the database."""

    def test_disc_detail_url(self):
        """Test that the disc detail URL resolves correctly."""
        url = reverse('disc_detail', kwargs={'disc_id': 1})
        self.assertEqual(url, '/discs/disc/1/')

    def test_submit_disc_url(self):
        """Test that the submit disc URL resolves correctly."""
        url = reverse('submit_disc')
        self.assertEqual(url, '/discs/submit-disc/')

class DiscURLTests(SimpleTestCase):

    def test_edit_disc_url_resolves(self):
        """Test that the edit_disc URL resolves correctly."""
        url = reverse('edit_disc', kwargs={'disc_id': 1})
        self.assertEqual(resolve(url).func, edit_disc)

class MapURLTests(SimpleTestCase):
    def test_disc_map_view_url_resolves(self):
        """Test that the disc map page URL resolves to the correct view."""
        url = reverse('disc_map_view')
        self.assertEqual(resolve(url).func, disc_map_view)

    def test_disc_map_api_url_resolves(self):
        """Test that the disc map API URL resolves to the correct view."""
        url = reverse('disc_map_api')
        self.assertEqual(resolve(url).func.view_class, DiscMapAPIView)