from django.db import models
from django.contrib.auth.models import User
from disc.models import Disc

class Message(models.Model):
    # User sending message
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    # User receiving message
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    # Optional reference to disc
    disc = models.ForeignKey(Disc, on_delete=models.SET_NULL, null=True, blank=True)
    # Message body
    content = models.TextField()
    # Timestamp of message used for notifications
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender} to {self.receiver} at {self.timestamp}"