# Zombie Discs

Zombie Discs is a web application built for the disc golf community to help recover lost discs and return them to their rightful owners. Players can log lost or found discs, set reward bounties, view matches based on color, location, and mold similarity, and communicate directly with each other through a built-in messaging system.

The platform features automatic disc matching logic, interactive maps, search and filtering tools, and user profile management — all designed to make disc recovery easy, community-driven, and rewarding.

## Features

- Log Lost or Found discs with optional photos and GPS location
- Optionally offer a reward for returning lost discs
- Intelligent disc matching algorithm based on color, type, mold, manufacturer, and proximity
- View matched discs and message the other user via a private inbox system
- View your active and archived discs on an interactive map
- Leaderboards for most discs lost, found, karma given, and rewards earned/offered
- Authentication, user profiles, and edit/delete controls for your own discs
- REST API endpoints for key data (discs, stats, map)

##Prerequisites

- Python 3.x
- Django
- Django REST Framework
- django-filter
- Leaflet.js (for maps)
- geopy (for distance calculations)
- difflib (for fuzzy matching)
- Pillow (for image uploads)

## Setup

1. **Clone the repository:**

   ```sh
    git clone https://github.com/yourusername/zombie-discs.git
    cd zombie-discs

2. **Create and activate a virtual environment:**

    ```sh
    python -m venv venv
    source venv/bin/activate       # Mac/Linux
    venv\Scripts\activate          # Windows

3. **Install dependencies:**

    ```sh
    pip install -r requirements.txt

4. **Set up environment variables:**

    Create a .env file in the root of the project and add your secret key:
    SECRET_KEY=your-new-secret-key

    You can generate a new Django secret key using the following Python script:
    
    ```sh
    from django.core.management.utils import get_random_secret_key
    print(get_random_secret_key())

5. **Apply migrations:**

    ```sh
    python manage.py makemigrations
    python manage.py migrate

6. **(Optional) Create a Superuser**

   ```sh
   python manage.py createsuperuser

7. **(Optional) Seed the Database**
   
   ```sh
    python manage.py loaddata db_seed.json
   
8. **Run the Development Server**
   
   ```sh
    python manage.py runserver

9. **(Optional) Run Tests to Confirm It Works**
   
   ```sh
    python manage.py test
