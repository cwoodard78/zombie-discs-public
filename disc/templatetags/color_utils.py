"""
Custom Django template filter to validate and represent disc colors.
- Returns RGBA values for valid colors with medium transparency.
- Generates a gradient for "Multi" discs and a hatched pattern for invalid or "Unknown" colors.
"""

from django import template

register = template.Library()

@register.filter
def validate_color(color):
    # List of valid CSS color names and corresponding rgba values
    valid_colors = {
        "red": "rgba(255, 0, 0, 0.4)",
        "blue": "rgba(0, 0, 255, 0.4)",
        "green": "rgba(0, 255, 0, 0.4)",
        "yellow": "rgba(255, 255, 0, 0.4)",
        "black": "rgba(0, 0, 0, 0.4)",
        "white": "rgba(255, 255, 255, 0.4)",
        "purple": "rgba(128, 0, 128, 0.4)",
        "orange": "rgba(255, 165, 0, 0.4)",
        "pink": "rgba(255, 192, 203, 0.4)",
        "gray": "rgba(128, 128, 128, 0.4)",
        "brown": "rgba(165, 42, 42, 0.4)",
        "cyan": "rgba(0, 255, 255, 0.4)",
        "magenta": "rgba(255, 0, 255, 0.4)",
        "lime": "rgba(0, 255, 0, 0.4)",
        "teal": "rgba(0, 128, 128, 0.4)",
        "navy": "rgba(0, 0, 128, 0.4)",
    }

    # Normalize the color to lowercase
    color = color.lower()

    if color in valid_colors:
        return valid_colors[color]

    # Multi color gradient for "Multi" color
    if color == "multi":
        return (
            "linear-gradient(45deg, "
            "rgba(255, 0, 0, 0.4), "
            "rgba(255, 165, 0, 0.4), "
            "rgba(255, 255, 0, 0.4), "
            "rgba(0, 255, 0, 0.4), "
            "rgba(0, 255, 255, 0.4), "
            "rgba(0, 0, 255, 0.4), "
            "rgba(128, 0, 128, 0.4))"
        )

    # Gray hatched pattern for "Unknown" or invalid colors
    return "repeating-linear-gradient(45deg, #cccccc, #cccccc 10px, #eeeeee 10px, #eeeeee 20px)"
