from django.forms.widgets import Widget
from django.utils.safestring import mark_safe
from .constants import COLOR_CHOICES
from .templatetags.color_utils import validate_color

class ColorGridWidget(Widget):
    """
    Widget that renders a color selection grid.
    Each color is represented as a rectangle with a color swatch and label.
    Used for selecting disc color in the submission form.
    """
    def render(self, name, value, attrs=None, renderer=None):
        # Responsive 6-column grid
        html = '<div class="grid grid-cols-6 gap-2">'
        # Loop thru predefined color list
        for color_value, color_name in COLOR_CHOICES:
            # Highlight selected color
            selected_class = 'ring-2 ring-blue-500' if value == color_value else ''
            style = f'background: {validate_color(color_value)};'

            # Build labels on custom radio input
            html += f'''
            <label class="color-option relative block text-center text-xs font-semibold text-gray-800 cursor-pointer p-2 rounded border border-gray-300 {selected_class}" 
                style="{style}">
                <input type="radio" name="{name}" value="{color_value}" class="sr-only color-radio" {'checked' if value == color_value else ''}>
                {color_name}
            </label>
            '''

        html += '</div>'
        return mark_safe(html)
