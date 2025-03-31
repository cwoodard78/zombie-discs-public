from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from inbox.models import Message
from disc.models import Disc

class InboxViewTests(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username='sender', password='pass')
        self.receiver = User.objects.create_user(username='receiver', password='pass')
        self.client.login(username='receiver', password='pass')

    def test_inbox_view_renders_template(self):
        response = self.client.get(reverse('inbox'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inbox/inbox.html')

    def test_send_message_view_get(self):
        response = self.client.get(reverse('send_message', args=[self.sender.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inbox/send_message.html')

    def test_send_message_view_post_creates_message(self):
        response = self.client.post(reverse('send_message', args=[self.sender.id]), {
            'content': 'Hello!'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after POST
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(Message.objects.first().content, 'Hello!')

    def test_send_message_with_disc_reference(self):
        disc = Disc.objects.create(user=self.receiver, status='lost', color='Red')
        response = self.client.post(
            reverse('send_message', args=[self.sender.id, disc.id]),
            {'content': 'I found your disc'}
        )
        self.assertEqual(Message.objects.first().disc, disc)

    def test_delete_message_view(self):
        msg = Message.objects.create(sender=self.sender, receiver=self.receiver, content="Hi")
        response = self.client.post(reverse('delete_message', args=[msg.id]))
        self.assertRedirects(response, reverse('inbox'))
        self.assertEqual(Message.objects.count(), 0)

    def test_non_owner_cannot_delete_message(self):
        other_user = User.objects.create_user(username='other', password='pass')
        msg = Message.objects.create(sender=self.sender, receiver=self.receiver, content="Hi")
        self.client.logout()
        self.client.login(username='other', password='pass')
        response = self.client.post(reverse('delete_message', args=[msg.id]))
        self.assertEqual(response.status_code, 404)  # Not their message
