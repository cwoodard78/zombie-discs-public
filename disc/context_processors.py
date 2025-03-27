from .models import Disc, DiscMatch
from django.utils.timezone import now

def match_notifications(request):
    if request.user.is_authenticated:
        discs = Disc.objects.filter(user=request.user)
        last_login = request.user.last_login or now()
        new_matches = 0

        for disc in discs:
            if disc.status == 'lost':
                matches = DiscMatch.objects.filter(lost_disc=disc)
            elif disc.status == 'found':
                matches = DiscMatch.objects.filter(found_disc=disc)
            else:
                continue

            if matches.filter(created_at__gt=last_login).exists():
                new_matches += 1

        return {'new_matches_count': new_matches}

    return {}