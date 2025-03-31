from django.core.management.base import BaseCommand
from disc.models import Disc
from disc.match_logic import populate_disc_matches

class Command(BaseCommand):
    """
    Custom Django management command to run the disc matching logic manually.
    
    This command fetches all lost and found discs from the database and uses the `populate_disc_matches` function to calculate and store potential matches based on defined scoring logic.
    
    Usage: python manage.py match_discs
    """
    help = 'Populate database with matches for lost and found discs'

    def handle(self, *args, **kwargs):
        lost_discs = Disc.objects.filter(status="lost")
        found_discs = Disc.objects.filter(status="found")

        populate_disc_matches(lost_discs, found_discs)
        self.stdout.write(self.style.SUCCESS("Matches have been updated in the database."))
