"""
Context Processor: Match Notifications

Adds `new_matches_count` to the template context for authenticated users. This allows the UI (e.g., the navigation bar) to display a notification badge when there are new potential disc matches since the user's last login.
"""

from .models import Disc, DiscMatch
from django.utils.timezone import now

def match_notifications(request):
    if request.user.is_authenticated:
        # Get all discs owned by the currently logged-in user
        discs = Disc.objects.filter(user=request.user)
        # Determine the user's last login time (fallback to now if not set)
        last_login = request.user.last_login or now()

        # Counter for new matches since last login
        new_matches = 0

        for disc in discs:
            # Fetch matches depending on whether this is a lost or found disc
            if disc.status == 'lost':
                matches = DiscMatch.objects.filter(lost_disc=disc)
            elif disc.status == 'found':
                matches = DiscMatch.objects.filter(found_disc=disc)
            else:
                continue    # Skip discs with other statuses

            # Count only matches created after the last login
            if matches.filter(created_at__gt=last_login).exists():
                new_matches += 1

        # Return the count to the templates
        return {'new_matches_count': new_matches}

    # If not authenticated, return an empty context
    return {}