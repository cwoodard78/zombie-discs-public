from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from disc.models import Disc, Manufacturer
from faker import Faker
import random

class Command(BaseCommand):
    help = "Seed the database with test users and discs (marked with _seed)"

    def add_arguments(self, parser):
        parser.add_argument('--users', type=int, default=1000, help='Number of users to create')
        parser.add_argument('--discs-per-user', type=int, default=10, help='Number of discs per user')

    def handle(self, *args, **options):
        fake = Faker()
        users = options['users']
        discs_per_user = options['discs_per_user']

        # Prepare options
        color_choices = [choice[0] for choice in Disc._meta.get_field('color').choices]
        status_choices = [choice[0] for choice in Disc._meta.get_field('status').choices]
        state_choices = [choice[0] for choice in Disc._meta.get_field('state').choices]
        type_choices = [choice[0] for choice in Disc._meta.get_field('type').choices if choice[0]]  # Exclude None
        manufacturers = list(Manufacturer.objects.all())

        self.stdout.write(f"Seeding {users} users with {discs_per_user} discs each...")

        for i in range(users):
            username = f"user{i}_seed"
            user = User.objects.create_user(
                username=username,
                email=f"{username}@example.com",
                password='test1234'
            )

            disc_list = []
            for _ in range(discs_per_user):
                disc = Disc(
                    user=user,
                    status=random.choice(status_choices),
                    state=random.choice(state_choices),
                    color=random.choice(color_choices),
                    type=random.choice(type_choices),
                    manufacturer=random.choice(manufacturers) if manufacturers else None,
                    mold_name=f"{fake.word().capitalize()}_seed",
                    notes=fake.sentence(),
                    latitude=round(random.uniform(30.0, 45.0), 6),
                    longitude=round(random.uniform(-90.0, -70.0), 6)
                    # created_at is auto
                )
                disc_list.append(disc)

            Disc.objects.bulk_create(disc_list)

        self.stdout.write(self.style.SUCCESS("✅ Done seeding! Records marked with '_seed'."))
