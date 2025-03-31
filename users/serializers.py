from rest_framework import serializers
from django.contrib.auth.models import User

# Serializer for the built-in Django User model
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User    # Built-in User model
        fields = ['username', 'email']