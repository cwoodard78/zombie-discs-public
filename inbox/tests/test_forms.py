from django.test import TestCase
from inbox.forms import MessageForm

class MessageFormTests(TestCase):
    def test_valid_message_form(self):
        form = MessageForm(data={'content': 'Hey!'})
        self.assertTrue(form.is_valid())

    def test_invalid_message_form(self):
        form = MessageForm(data={'content': ''})
        self.assertFalse(form.is_valid())
