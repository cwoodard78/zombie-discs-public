from django.db.models.signals import post_save
from django.dispatch import receiver
from disc.models import Disc
from disc.match_logic import populate_disc_matches

@receiver(post_save, sender=Disc)
def run_matching_on_save(sender, instance, **kwargs):
    from disc.models import Disc  # circular import protection

    if instance.status == "lost":
        lost_discs = [instance]
        found_discs = Disc.objects.filter(status="found")
    elif instance.status == "found":
        found_discs = [instance]
        lost_discs = Disc.objects.filter(status="lost")
    else:
        return

    populate_disc_matches(lost_discs, found_discs)