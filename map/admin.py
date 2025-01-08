from django.contrib import admin
from .models import Disc

# Register your models here.
@admin.register(Disc)
class DiscAdmin(admin.ModelAdmin):
    list_display = ('status', 'color', 'latitude', 'longitude', 'created_at')
    list_filter = ('status', 'color', 'created_at')
    search_fields = ('notes',)