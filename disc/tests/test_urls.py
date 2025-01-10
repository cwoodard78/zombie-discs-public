from django.test import SimpleTestCase
from django.urls import reverse, resolve
from disc.views import submit_disc, map_view

class DiscURLTests(SimpleTestCase):

    def test_submit_disc_url_resolves(self):
        """Test that the submit_disc URL resolves correctly."""
        url = reverse('submit_disc')
        self.assertEqual(resolve(url).func, submit_disc)

    def test_map_view_url_resolves(self):
        """Test that the map_view URL resolves correctly."""
        url = reverse('map_view')
        self.assertEqual(resolve(url).func, map_view)
