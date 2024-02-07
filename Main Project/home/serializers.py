from rest_framework import serializers
from .models import CustomUser

class PoliceOfficerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'name')