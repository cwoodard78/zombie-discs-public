from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    """
    Form for composing and sending a message. 
    Only the content field is exposed to the user.
    """
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your message...'}),
        }