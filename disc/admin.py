from django.contrib import admin
from .models import Disc, Manufacturer

# Register your models here.
@admin.register(Disc)
class DiscAdmin(admin.ModelAdmin):
    list_display = ('status', 'color', 'type', 'mold_name', 'latitude', 'longitude', 'user', 'created_at')
    search_fields = ('color', 'mold_name', 'user__username')
    list_filter = ('status', 'type', 'manufacturer', 'created_at')

@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Display the name column in the admin list view
    search_fields = ('name',)  # Add a search bar for the name field