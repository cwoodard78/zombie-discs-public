from rest_framework import serializers
from .models import Disc
from django.contrib.auth.models import User

class DiscSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disc
        fields = '__all__'

class StatsSerializer(serializers.Serializer):
    total_lost = serializers.IntegerField()
    total_found = serializers.IntegerField()
    total_users = serializers.IntegerField()

class RecentDiscSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    
    class Meta:
        model = Disc
        fields = ['id', 'status', 'color', 'type', 'manufacturer', 'mold_name', 'notes', 'latitude', 'longitude', 'created_at', 'user']

class DiscMapSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    manufacturer = serializers.StringRelatedField()  # String representation of manufacturer

    class Meta:
        model = Disc
        fields = [
            'id', 'status', 'color', 'latitude', 'longitude', 
            'notes', 'username', 'manufacturer'
        ]

# class DiscMapSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Disc
#         fields = ['id', 'status', 'color', 'latitude', 'longitude', 'notes', 'manufacturer']