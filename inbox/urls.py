"""
Inbox App URL Configuration

Defines URL routes for messaging functionality within the Zombie Discs app:
- Sending messages to other users
- Viewing the user's inbox
- Deleting messages
"""

from django.urls import path
from . import views

urlpatterns = [
    # Send a message to a user about a specific disc
    path('inbox/<int:receiver_id>/<int:disc_id>/', views.send_message, name='send_message'),
    # Send a general message to a user (no disc_id)
    path('inbox/<int:receiver_id>/', views.send_message, name='send_message'),
    # View the user's inbox
    path('inbox/', views.inbox_view, name='inbox'),
    # Delete specific message from the inbox
    path('inbox/delete/<int:message_id>/', views.delete_message, name='delete_message'),
]
