from django.contrib import admin
from .models import Disc, Manufacturer, DiscMatch, Reward

@admin.register(Disc)
class DiscAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'color', 'type', 'mold_name', 'latitude', 'longitude', 'user', 'created_at')
    search_fields = ('color', 'mold_name', 'user__username')
    list_filter = ('status', 'type', 'manufacturer', 'created_at')

@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Display the name column in the admin list view
    search_fields = ('name',)  # Add a search bar for the name field

@admin.register(DiscMatch)
class DiscMatchAdmin(admin.ModelAdmin):
    list_display = ('lost_disc','found_disc','score',)

@admin.register(Reward) 
class RewardAdmin(admin.ModelAdmin):
    list_display = ('disc', 'amount', 'created_at')
    search_fields = ('disc__mold_name', 'disc__user__username')
    list_filter = ('created_at',)