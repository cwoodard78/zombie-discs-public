# import_profiles.py

import os
import json
from pathlib import Path

# Step 1: Configure Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "zombie.settings")

import django
django.setup()

# Step 2: Now that Django is setup, import models
from django.contrib.auth.models import User
from users.models import Profile

def import_profiles_from_fixture():
    fixture_path = Path(__file__).resolve().parent / 'fixtures' / 'profiles.json'

    if not fixture_path.exists():
        print("❌ profiles.json not found in fixtures folder.")
        return

    with open(fixture_path, 'r', encoding='utf-8') as f:
        profiles = json.load(f)

    created, updated, skipped = 0, 0, 0

    for entry in profiles:
        user_id = entry["fields"]["user"]
        karma = entry["fields"].get("karma", 0)
        photo = entry["fields"].get("photo", None)

        try:
            user = User.objects.get(pk=user_id)
            profile, is_created = Profile.objects.update_or_create(
                user=user,
                defaults={"karma": karma, "photo": photo}
            )
            if is_created:
                created += 1
            else:
                updated += 1
        except User.DoesNotExist:
            print(f"⚠️ Skipped: No user with ID {user_id}")
            skipped += 1

    print(f"Done! Created: {created}, Updated: {updated}, Skipped: {skipped}")

if __name__ == "__main__":
    import_profiles_from_fixture()
