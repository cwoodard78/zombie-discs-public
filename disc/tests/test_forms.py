from django.test import TestCase
from disc.forms import DiscForm
from disc.models import Manufacturer
from django.core.files.uploadedfile import SimpleUploadedFile

class DiscFormTests(TestCase):

    def setUp(self):
        """Set up reusable objects."""
        self.manufacturer = Manufacturer.objects.create(name="Innova")

    def test_disc_form_valid(self):
        """Test that the form is valid with correct data."""
        form_data = {
            'status': 'lost',
            'color': 'Red',
            'type': 'Driver',
            'manufacturer': self.manufacturer.id,
            'mold_name': 'Destroyer',
            'notes': 'Left in the bushes near hole 5.',
            'latitude': 34.89495,
            'longitude': -86.44408,
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

    def test_disc_form_invalid_latitude_longitude(self):
        """Test that the form is invalid with invalid latitude or longitude."""
        form_data = {
            'status': 'lost',
            'color': 'Blue',
            'type': 'midrange',
            'manufacturer': self.manufacturer.id,
            'mold_name': 'Roc',
            'latitude': 'invalid',  # Invalid latitude
            'longitude': -86.44408,
        }
        form = DiscForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('latitude', form.errors)

        form_data['latitude'] = 34.89495
        form_data['longitude'] = 'invalid'  # Invalid longitude
        form = DiscForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('longitude', form.errors)

    def test_disc_form_optional_fields(self):
        """Test that the form is valid without optional fields."""
        form_data = {
            'status': 'found',
            'color': 'Green',
            'latitude': 34.89495,
            'longitude': -86.44408,
        }
        form = DiscForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_disc_form_invalid_status(self):
        """Test that the form is invalid with an invalid status."""
        form_data = {
            'status': 'invalid_status',  # Invalid status
            'color': 'Yellow',
            'latitude': 34.89495,
            'longitude': -86.44408,
        }
        form = DiscForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('status', form.errors)

    def test_disc_form_long_mold_name(self):
        """Test that the form is invalid if the mold name exceeds max length."""
        form_data = {
            'status': 'found',
            'color': 'White',
            'type': 'putter',
            'manufacturer': self.manufacturer.id,
            'mold_name': 'A' * 101,  # Exceeds typical max length for mold name
            'latitude': 34.89495,
            'longitude': -86.44408,
        }
        form = DiscForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('mold_name', form.errors)

    def test_disc_form_invalid_manufacturer(self):
        """Test that the form is invalid if manufacturer does not exist."""
        form_data = {
            'status': 'lost',
            'color': 'Purple',
            'type': 'other',
            'manufacturer': 999,  # Non-existent manufacturer ID
            'latitude': 34.89495,
            'longitude': -86.44408,
        }
        form = DiscForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('manufacturer', form.errors)

    def test_disc_form_invalid_image_type(self):
        """Test that the form rejects an invalid image type."""
        invalid_image = SimpleUploadedFile("invalid_image.txt", b"file_content", content_type="text/plain")
        form_data = {
            'status': 'lost',
            'color': 'Yellow',
            'notes': 'Near hole 3.',
            'latitude': 34.89700,
            'longitude': -86.44600,
            'manufacturer': self.manufacturer.id,
            'mold_name': 'TeeBird',
        }
        form_files = {
            'image': invalid_image,
        }
        form = DiscForm(data=form_data, files=form_files)
        self.assertFalse(form.is_valid())
        self.assertIn('image', form.errors)