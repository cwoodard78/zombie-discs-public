from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from disc.models import Disc

class Command(BaseCommand):
    help = "Delete all seeded users and discs marked with '_seed'"

    def handle(self, *args, **kwargs):
        self.stdout.write("🧹 Deleting seeded discs...")
        Disc.objects.filter(mold_name__endswith="_seed").delete()

        self.stdout.write("🧹 Deleting seeded users...")
        User.objects.filter(username__endswith="_seed").delete()

        self.stdout.write(self.style.SUCCESS("✅ Seed data removed."))
