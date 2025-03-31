# Create the fixtures directory if it doesn't exist
if (!(Test-Path -Path "./fixtures")) {
    New-Item -ItemType Directory -Path "./fixtures"
}

Write-Output "Exporting fixture data..."

# Export each app's model data to its own JSON file
python manage.py dumpdata users.Profile --indent 2 > .\fixtures\profiles.json
python manage.py dumpdata auth.User --indent 2 > .\fixtures\users.json
python manage.py dumpdata inbox.Message --indent 2 > .\fixtures\messages.json
python manage.py dumpdata disc.Manufacturer --indent 2 > .\fixtures\manufacturers.json
python manage.py dumpdata disc.Disc --indent 2 > .\fixtures\discs.json
python manage.py dumpdata disc.DiscMatch --indent 2 > .\fixtures\matches.json
python manage.py dumpdata disc.Reward --indent 2 > .\fixtures\rewards.json

Write-Output "Export complete. Files saved to .\fixtures"
