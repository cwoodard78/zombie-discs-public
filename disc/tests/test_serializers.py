from django.test import TestCase
from disc.models import Disc, User
from disc.serializers import DiscMapSerializer

class DiscMapSerializerTests(TestCase):
    def test_disc_map_serializer(self):
        """Test the serializer outputs correct fields."""
        user = User.objects.create_user(username='testuser', password='password')
        disc = Disc.objects.create(
            user=user, status='lost', color='Red', latitude=34.1, longitude=-86.1, notes='Test disc'
        )
        serializer = DiscMapSerializer(disc)
        data = serializer.data

        self.assertEqual(data['status'], 'lost')
        self.assertEqual(data['latitude'], 34.1)
        self.assertEqual(data['longitude'], -86.1)
        self.assertEqual(data['notes'], 'Test disc')
        self.assertIn('username', data)
