from django.db import models
from django.contrib.auth.models import User

class MyModel(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

class Disc(models.Model):
    STATUS_CHOICES = [
        ('lost', 'Lost'),
        ('found', 'Found'),
    ]

    DISC_TYPE_CHOICES = [
        ('driver', 'Driver'),
        ('midrange', 'Midrange'),
        ('putter', 'Putter'),
        ('other', 'Other'),
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Tie to authenticated user

    def __str__(self):
        return f"{self.get_status_display()} disc - {self.color}"
    
# Separate table for disc manufacturers for scalability
class Manufacturer(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name