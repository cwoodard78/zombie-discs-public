"""
DiscForm Definition

This form is used to create and update Disc instances, including custom widgets such as a color selection grid and hidden latitude/longitude fields for map input.
"""

from django import forms
from .models import Disc
from .widgets import ColorGridWidget

class DiscForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['color'].initial = 'unknown'  # default to "Unknown" color to avoid submission errors

    class Meta:
        model = Disc
        fields = ['status', 'color', 'type', 'manufacturer', 'mold_name', 'notes', 'latitude', 'longitude', 'image']
        widgets = {
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
            'color': ColorGridWidget(),  # Use the custom color grid
            'notes': forms.Textarea(attrs={'rows': 3}),
        }