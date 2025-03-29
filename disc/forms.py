from django import forms
from .models import Disc
from .widgets import ColorGridWidget
class DiscForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['color'].initial = 'unknown'  # default to "Unknown" color to avoid errors

    class Meta:
        model = Disc
        fields = ['status', 'color', 'type', 'manufacturer', 'mold_name', 'notes', 'latitude', 'longitude', 'image']
        widgets = {
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
            'color': ColorGridWidget(),  # Use the custom color grid
            'notes': forms.Textarea(attrs={'rows': 3}),
        }