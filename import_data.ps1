# Step 1: Load fixtures (excluding profiles)
$fixtures = @(
    "users.json",        # Create users first
    "manufacturers.json",
    "discs.json",
    "messages.json",
    "rewards.json"
)

Write-Output "Importing fixture data..."

foreach ($fixture in $fixtures) {
    $path = ".\fixtures\$fixture"
    if (Test-Path $path) {
        Write-Output "Loading $fixture..."
        python manage.py loaddata $path
    } else {
        Write-Output "Skipping $fixture (not found)"
    }
}

# Step 2: Load profiles separately (after users)
Write-Host "Running import_profiles.py to attach profiles..."
python import_profiles.py

# Step 3: Run match logic to regenerate disc matches
Write-Host "Running match_discs command to populate matches..."
python manage.py match

Write-Output "Import complete."
