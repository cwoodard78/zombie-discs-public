from django.test import TestCase
from disc.forms import DiscForm
from disc.models import Manufacturer

class DiscFormTests(TestCase):

    def test_disc_form_valid(self):
        """Test that the form is valid with correct data."""
        manufacturer = Manufacturer.objects.create(name="Innova")
        form_data = {
            'status': 'lost',
            'color': 'Red',
            'notes': 'Left in the bushes near hole 5.',
            'latitude': 34.89495,
            'longitude': -86.44408,
            'disc_type': 'driver',
            'manufacturer': manufacturer.id,
            'mold_name': 'Destroyer',
        }
        form = DiscForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_disc_form_missing_fields(self):
        """Test that the form is invalid if required fields are missing."""
        form_data = {
            'status': 'lost',
            'color': '',  # Missing color
            'latitude': 34.89495,
            'longitude': -86.44408,
        }
        form = DiscForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('color', form.errors)
