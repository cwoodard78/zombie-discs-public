from django.db import models
from django.contrib.auth.models import User

# Extension of the User model for additional user data
class Profile(models.Model):
    # One-to-one; each user gets one profile
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # Optional photo
    photo = models.ImageField(upload_to='user_photos/', blank=True, null=True)
    # Karma points tracker
    karma = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s Profile"