from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# class MyModel(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.TextField()

class Disc(models.Model):
    STATUS_CHOICES = [
        ('lost', 'Lost'),
        ('found', 'Found'),
    ]

    DISC_TYPE_CHOICES = [
        ('Driver', 'Driver'),
        ('Midrange', 'Midrange'),
        ('Putter', 'Putter'),
        ('Other', 'Other'),
    ]

    status = models.CharField(max_length=5, choices=STATUS_CHOICES, default='lost')
    color = models.CharField(max_length=50)
    type = models.CharField(max_length=10, choices=DISC_TYPE_CHOICES, blank=True, null=True)
    manufacturer = models.ForeignKey(
        'Manufacturer', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    mold_name = models.CharField(max_length=100, blank=True, null=True)  # Free-text field for mold name
    notes = models.TextField(blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='disc_images/', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Tie to authenticated user

    def __str__(self):
        return f"{self.get_status_display()} disc - {self.color}"
    
# Separate table for disc manufacturers for scalability
class Manufacturer(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class DiscMatch(models.Model):
    lost_disc = models.ForeignKey('Disc', on_delete=models.CASCADE, related_name='lost_matches')
    found_disc = models.ForeignKey('Disc', on_delete=models.CASCADE, related_name='found_matches')
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ensures each pair of lost and found discs can only appear once in the table.
        unique_together = ('lost_disc', 'found_disc')
        ordering = ['-score']  # Order by score, highest first

    def __str__(self):
        return f"Match: Lost Disc {self.lost_disc.id} - Found Disc {self.found_disc.id} (Score: {self.score})"
    
class Reward(models.Model):
    disc = models.OneToOneField(Disc, on_delete=models.CASCADE, related_name='reward')
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)