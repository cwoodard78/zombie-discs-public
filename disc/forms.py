from django import forms
from .models import Disc

class DiscForm(forms.ModelForm):
    class Meta:
        model = Disc
        fields = ['status', 'color', 'type', 'manufacturer', 'mold_name', 'notes', 'latitude', 'longitude']
        widgets = {
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
        }