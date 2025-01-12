from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from disc.models import Disc
from django.contrib.auth.models import User
from django.utils import timezone

class DiscAPITests(APITestCase):

    def setUp(self):
        # Clear existing discs
        Disc.objects.all().delete()

        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")

        # Create test discs
        self.disc1 = Disc.objects.create(
            user=self.user, 
            status="lost", 
            color="Red", 
            notes="Lost near hole 1", 
            latitude=34.1, 
            longitude=-86.1,
        )
        # Override Django auto_now_add behavior. Change disc created_at date
        self.disc1.created_at = timezone.now() - timezone.timedelta(days=1)  # Older timestamp
        self.disc1.save(update_fields=["created_at"])

        self.disc2 = Disc.objects.create(
            user=self.user, 
            status="found", 
            color="Blue", 
            notes="Found near hole 3", 
            latitude=0, 
            longitude=0,
        )

    def test_get_all_discs(self):
        """Test retrieving all discs"""
        url = reverse("disc_list_api")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_post_create_disc(self):
        """Test creating a new disc"""
        url = reverse("disc_list_api")
        data = {
            "status": "lost",
            "color": "Yellow",
            "notes": "Near hole 5",
            "latitude": 0,
            "longitude": 0,
            "user": self.user.id,  # Include the user if it's required
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Disc.objects.count(), 3)

    def test_get_disc_detail(self):
        """Test retrieving a single disc's details"""
        url = reverse("disc_detail_api", kwargs={"pk": self.disc1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["color"], "Red")

    def test_update_disc(self):
        """Test updating a disc"""
        url = reverse("disc_detail_api", kwargs={"pk": self.disc1.id})
        data = {"color": "Green"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.disc1.refresh_from_db()
        self.assertEqual(self.disc1.color, "Green")

    def test_delete_disc(self):
        """Test deleting a disc"""
        url = reverse("disc_detail_api", kwargs={"pk": self.disc1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Disc.objects.count(), 1)

    def test_get_recent_discs(self):
        """Test retrieving the most recent discs"""
        url = reverse("recent_discs_api")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["notes"], "Found near hole 3")  # Most recent

    def test_get_stats(self):
        """Test retrieving disc statistics"""
        url = reverse("stats_api")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_lost"], 1)
        self.assertEqual(response.data["total_found"], 1)
        self.assertEqual(response.data["total_users"], 1)
