"""
Context Processor for Message Notifications
This is used to display a notification indicator in the navigation bar.
"""

from inbox.models import Message

def unread_message_count(request):
    """
    Return the count of unread messages for authenticated users.
    Messages is 'unread' if sent after user's last login.
    """
    if request.user.is_authenticated:
        return {
            'unread_count': Message.objects.filter(
                receiver=request.user,
                timestamp__gt=request.user.last_login
            ).count()
        }
    return {}
