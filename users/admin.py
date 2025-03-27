# from django.contrib import admin

# # Register your models here.

from django.contrib import admin
from .models import Profile
from disc.models import Disc

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'karma', 'lost_total', 'found_total')

    def lost_total(self, obj):
        return Disc.objects.filter(user=obj.user, status='lost').count()
    lost_total.short_description = 'Lost Discs'

    def found_total(self, obj):
        return Disc.objects.filter(user=obj.user, status='found').count()
    found_total.short_description = 'Found Discs'

admin.site.register(Profile, ProfileAdmin)