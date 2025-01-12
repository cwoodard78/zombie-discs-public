from rest_framework import serializers
from .models import Disc
# from .models import MyModel
from django.contrib.auth.models import User

# class MyModelSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = MyModel
#         fields = '__all__'

class DiscSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disc
        fields = '__all__'

class StatsSerializer(serializers.Serializer):
    total_lost = serializers.IntegerField()
    total_found = serializers.IntegerField()
    total_users = serializers.IntegerField()

class RecentDiscSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Will use the `__str__` method of the `User` model
    
    class Meta:
        model = Disc
        fields = ['id', 'status', 'color', 'type', 'manufacturer', 'mold_name', 'notes', 'latitude', 'longitude', 'created_at', 'user']