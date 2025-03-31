from django.contrib import admin
from .models import Profile
from disc.models import Disc

# Custom admin configuration for the Profile model
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'karma', 'lost_total', 'found_total')

    def lost_total(self, obj):
        """
        Returns the number of 'lost' discs associated with the user.
        """
        return Disc.objects.filter(user=obj.user, status='lost').count()
    lost_total.short_description = 'Lost Discs'

    def found_total(self, obj):
        """
        Returns the number of 'found' discs associated with the user.
        """
        return Disc.objects.filter(user=obj.user, status='found').count()
    found_total.short_description = 'Found Discs'

admin.site.register(Profile, ProfileAdmin)