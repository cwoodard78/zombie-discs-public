import os
import subprocess

FIXTURES_DIR = os.path.join('.', 'fixtures')
FIXTURES = [
    "users.json",         # Users first
    "manufacturers.json",
    "discs.json",
    "messages.json",
    "rewards.json"
]

def run_command(command, description=None):
    if description:
        print(f"\n{description}")
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running: {command}\n{e}")

def load_fixtures():
    print("Importing fixture data...")
    for fixture in FIXTURES:
        path = os.path.join(FIXTURES_DIR, fixture)
        if os.path.exists(path):
            run_command(f"python manage.py loaddata {path}", f"Loading {fixture}...")
        else:
            print(f"Skipping {fixture} (not found)")

def run_profile_import():
    run_command("python import_profiles.py", "Attaching profiles to users...")

def run_match_logic():
    run_command("python manage.py match", "Running match logic to regenerate matches...")

if __name__ == "__main__":
    load_fixtures()
    run_profile_import()
    run_match_logic()
    print("Import complete.")
