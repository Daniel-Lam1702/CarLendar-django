from cars.models import Car  # Import the Car model
from rest_framework import serializers
class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = "__all__"