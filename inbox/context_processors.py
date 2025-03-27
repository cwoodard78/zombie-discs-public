from inbox.models import Message

def unread_message_count(request):
    if request.user.is_authenticated:
        return {
            'unread_count': Message.objects.filter(
                receiver=request.user,
                timestamp__gt=request.user.last_login
            ).count()
        }
    return {}
