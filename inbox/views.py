from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import MessageForm
from inbox.models import Message

@login_required
def send_message(request, receiver_id, disc_id=None):
    """
    View to send a private message to another user.
    Optionally includes a reference to a disc.
    """
    receiver = get_object_or_404(User, id=receiver_id)

    # Handle redirect URL
    if request.method == "GET":
        next_url = request.META.get("HTTP_REFERER", "")
    else:
        next_url = request.POST.get("next", "")

    form = MessageForm(request.POST or None)

    if form.is_valid():
        message = form.save(commit=False)
        message.sender = request.user
        message.receiver = receiver
        # Only import when needed, not all messages are disc related
        if disc_id:
            from disc.models import Disc
            message.disc = get_object_or_404(Disc, id=disc_id)
        message.save()

        # Redirect to the original page if available
        # Alternatively fallback to receiver's profile
        if next_url:
            return redirect(next_url)
        return redirect('profile', username=receiver.username)

    return render(request, 'inbox/send_message.html', {
        'form': form,
        'receiver': receiver,
        'next': next_url
    })

@login_required
def inbox_view(request):
    """
    Displays all received messages for the authenticated user.
    Ordered by most recent first.
    """
    user = request.user
    messages = Message.objects.filter(receiver=user).select_related('sender', 'disc').order_by('-timestamp')

    return render(request, 'inbox/inbox.html', {
        'messages': messages,
    })

@login_required
def delete_message(request, message_id):
    """
    Allows the recipient to delete a message.
    Only allows deletion by the message's receiver.
    """
    message = get_object_or_404(Message, id=message_id, receiver=request.user)
    if request.method == 'POST':
        message.delete()
    return redirect('inbox')