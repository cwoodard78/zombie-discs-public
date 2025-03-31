"""
Color Constants for Disc Classification

This file defines the standardized list of valid disc colors used throughout the application.
- `VALID_COLORS`: A human-readable list aligned with frontend display and internal logic (e.g., color_utils.py).
- `COLOR_CHOICES`: A lowercased tuple list derived from VALID_COLORS, used in model and form field `choices`.

Ensure consistency between this list and the logic in any color matching or display utilities.
"""

VALID_COLORS = [
    "Red", 
    "Orange", 
    "Yellow", 
    "Green", 
    "Blue", 
    "Purple", 
    "Pink", 
    "Black", 
    "Brown", 
    "Gray", 
    "White", 
    "Multi", 
    "Unknown",
    # Other available default colors if needed. Not used to help converge colors to yield more matches.
    # "Cyan", 
    # "Magenta", 
    # "Lime", 
    # "Teal", 
    # "Navy", 
]

COLOR_CHOICES = [(color.lower(), color) for color in VALID_COLORS]