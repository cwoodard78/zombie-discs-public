from rest_framework import serializers
from .models import Disc
from django.contrib.auth.models import User

# Full Serializer for Disc model (used in API CRUD operations)
class DiscSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disc
        fields = '__all__'

# Simple serializer for dashboard statistics
# (Used in StatsAPIView to return custom summary data)
class StatsSerializer(serializers.Serializer):
    total_lost = serializers.IntegerField()
    total_found = serializers.IntegerField()
    total_users = serializers.IntegerField()

# Streamlined serializer for displaying recent discs
# (Used in RecentDiscsAPIView)
class RecentDiscSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    
    class Meta:
        model = Disc
        fields = ['id', 'status', 'color', 'type', 'manufacturer', 'mold_name', 'notes', 'latitude', 'longitude', 'created_at', 'user']

# Serializer for displaying discs on a map
# (Used in DiscMapAPIView and DiscSearchView with map overlay)
class DiscMapSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    manufacturer = serializers.StringRelatedField()  # String representation of manufacturer

    class Meta:
        model = Disc
        fields = [
            'id', 'status', 'color', 'latitude', 'longitude', 
            'notes', 'username', 'manufacturer'
        ]