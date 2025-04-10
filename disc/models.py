from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from .constants import COLOR_CHOICES

# Main model representing a lost or found disc
class Disc(models.Model):
    STATUS_CHOICES = [
        ('lost', 'Lost'),
        ('found', 'Found'),
    ]

    RECORD_STATE_CHOICES = [
        ('active', 'Active'),
        ('returned', 'Returned'),  # Successfully resolved
        ('archived', 'Archived'),  # No longer tracked
    ]

    DISC_TYPE_CHOICES = [
        ('Driver', 'Driver'),
        ('Midrange', 'Midrange'),
        ('Putter', 'Putter'),
        ('Other', 'Other'),
    ]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='lost')
    state = models.CharField(max_length=10, choices=RECORD_STATE_CHOICES, default='active')
    # User standard colors from templatetags
    color = models.CharField(max_length=20, choices=COLOR_CHOICES)
    type = models.CharField(max_length=10, choices=DISC_TYPE_CHOICES, blank=True, null=True)
    manufacturer = models.ForeignKey(
        'Manufacturer', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    # Optional
    mold_name = models.CharField(max_length=100, blank=True, null=True)  # Free-text field for mold name
    notes = models.TextField(blank=True, null=True)
    # Location default middle of the ocean (0,0)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)

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
    
# Table for potential lost/found disc matches
class DiscMatch(models.Model):
    lost_disc = models.ForeignKey('Disc', on_delete=models.CASCADE, related_name='lost_matches')
    found_disc = models.ForeignKey('Disc', on_delete=models.CASCADE, related_name='found_matches')
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Prvent duplicates.
        unique_together = ('lost_disc', 'found_disc')
        ordering = ['-score']  # Order by score, highest first

    def __str__(self):
        return f"Match: Lost Disc {self.lost_disc.id} - Found Disc {self.found_disc.id} (Score: {self.score})"
    
# Optional reward (bounty) offered for a lost disc
# Rewards are one-to-one with a disc
class Reward(models.Model):
    disc = models.OneToOneField(Disc, on_delete=models.CASCADE, related_name='reward')
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)