from django.core.management.base import BaseCommand
from disc.models import Disc, DiscMatch
# Allow for typos in mold name
from difflib import SequenceMatcher
# Calculate distances between coordinates
from geopy.distance import geodesic

class Command(BaseCommand):
    help = 'Populate database with matches for lost and found discs'

    def handle(self, *args, **kwargs):
        lost_discs = Disc.objects.filter(status="lost")
        found_discs = Disc.objects.filter(status="found")

        # Call function to find matches and save them
        populate_disc_matches(lost_discs, found_discs)
        self.stdout.write(self.style.SUCCESS("Matches have been updated in the database."))


def calculate_proximity_score(lat1, lon1, lat2, lon2):
    distance_km = geodesic((lat1, lon1), (lat2, lon2)).km
    if distance_km <= 2:  # 1 km radius
        return 50
    elif distance_km <= 10:  # 10 km radius
        return 25
    return 0

def calculate_match_score(lost_disc, found_disc):
    score = 0

    # Check color
    if lost_disc.color and found_disc.color:
        if lost_disc.color.lower() == found_disc.color.lower():
            score += 30  # Full points for color match
        else:
            score -= 10  # Penalty for mismatch

    # Check type
    if lost_disc.type and found_disc.type:
        if lost_disc.type.lower() == found_disc.type.lower():
            score += 20

    # Check manufacturer
    if lost_disc.manufacturer and found_disc.manufacturer:
        if (
            lost_disc.manufacturer.name.lower() == found_disc.manufacturer.name.lower()
        ):  # Access related object's name
            score += 20

    # Check mold name with fuzzy matching
    if lost_disc.mold_name and found_disc.mold_name:
        similarity = SequenceMatcher(None, lost_disc.mold_name.lower(), found_disc.mold_name.lower()).ratio()
        if similarity >= 0.9:  # High similarity
            score += 50
        elif similarity >= 0.7:  # Medium similarity
            score += 25

    # Calculate proximity score
    score += calculate_proximity_score(
        lost_disc.latitude,
        lost_disc.longitude,
        found_disc.latitude,
        found_disc.longitude,
    )

    return score

# Function to populate matches in the database
def populate_disc_matches(lost_discs, found_discs):
    for lost_disc in lost_discs:
        for found_disc in found_discs:
            score = calculate_match_score(lost_disc, found_disc)
            if score > 50:  # Only keep significant matches
                DiscMatch.objects.update_or_create(
                    lost_disc=lost_disc,
                    found_disc=found_disc,
                    defaults={'score': score}
                )

# from .models import Disc

# # Example: Fetch lost and found discs from your database
# lost_discs = Disc.objects.filter(status="lost")
# found_discs = Disc.objects.filter(status="found")

# # Find and rank matches
# matches = find_matches(lost_discs, found_discs)

# # Display results
# for match in matches:
#     print(f"Lost Disc ID: {match['lost_disc'].id}, Found Disc ID: {match['found_disc'].id}, Score: {match['score']}")

