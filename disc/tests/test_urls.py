from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve
from disc.views import (
    submit_disc,
    edit_disc,
    disc_map_view,
    DiscMapAPIView,
    disc_detail_view,
)

class DiscURLRoutingTests(SimpleTestCase):
    """
    Tests that do not hit the database — validating URL patterns and view resolution.
    """

    def test_submit_disc_url_resolves_to_view(self):
        url = reverse('submit_disc')
        self.assertEqual(resolve(url).func, submit_disc)

    def test_edit_disc_url_resolves_to_view(self):
        url = reverse('edit_disc', kwargs={'disc_id': 1})
        self.assertEqual(resolve(url).func, edit_disc)

    def test_disc_map_view_url_resolves(self):
        url = reverse('disc_map_view')
        self.assertEqual(resolve(url).func, disc_map_view)

    def test_disc_map_api_url_resolves_to_class_view(self):
        url = reverse('disc_map_api')
        self.assertEqual(resolve(url).func.view_class, DiscMapAPIView)

    def test_disc_detail_url_resolves_to_updated_view(self):
        url = reverse('disc_detail', kwargs={'disc_id': 1})
        self.assertEqual(resolve(url).func, disc_detail_view)


class DiscURLDatabaseTests(TestCase):
    """
    Tests that use the database to validate URL output.
    """

    def test_submit_disc_url_reverse(self):
        url = reverse('submit_disc')
        self.assertEqual(url, '/discs/submit-disc/')

    def test_disc_detail_url_reverse(self):
        url = reverse('disc_detail', kwargs={'disc_id': 1})
        self.assertEqual(url, '/discs/disc/1/')

    def test_edit_disc_url_reverse(self):
        url = reverse('edit_disc', kwargs={'disc_id': 42})
        self.assertEqual(url, '/discs/disc/42/edit/')
