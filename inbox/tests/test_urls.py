from django.test import SimpleTestCase
from django.urls import reverse, resolve
from inbox.views import send_message, inbox_view, delete_message

class InboxURLTests(SimpleTestCase):
    def test_inbox_url_resolves(self):
        url = reverse('inbox')
        self.assertEqual(resolve(url).func, inbox_view)

    def test_send_message_url_resolves(self):
        url = reverse('send_message', args=[1])
        self.assertEqual(resolve(url).func, send_message)

    def test_delete_message_url_resolves(self):
        url = reverse('delete_message', args=[1])
        self.assertEqual(resolve(url).func, delete_message)