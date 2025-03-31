"""
Template filter for dictionary key lookup, used in match notifications.

This custom filter is particularly useful in templates like 'user_disc_list.html' where we check if a specific disc has new matches by looking up a disc's ID in a dictionary (`match_flags`) passed from the view.

Example usage in template:
    {% if match_flags|dict_key:disc.id %} ... {% endif %}
"""

from django import template

register = template.Library()

@register.filter
def dict_key(d, key):
    """
    Safely retrieves the value for a given key from a dictionary.
    Used for checking match flags by disc ID in templates.
    """
    try:
        return d.get(key)
    except (AttributeError, TypeError):
        return None
