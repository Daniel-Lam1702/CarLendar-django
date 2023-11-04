from rest_framework import serializers
from .models import User_and_Car, Fix
from cars.serializers import CarSerializer
from users.serializers import UserSerializer
import requests

class User_Car_Serializer(serializers.ModelSerializer):
    car = CarSerializer(source='car_id', read_only=True)
    user = UserSerializer(source='user_id', read_only=True)

    class Meta:
        model = User_and_Car
        fields = ['id', 'user_id', 'car_id', 'vin', 'mileage', 'year', 'car']
    
    def validate_vin(self, vin):
        # Get the value of the 'year' field from the instance
        year = self.instance.year

        # Define VIN length conditions
        if year and year >= 1981:
            expected_length = 17
        else:
            expected_length = (11, 17)

        if len(vin) not in expected_length:
            raise serializers.ValidationError("Invalid VIN length for the given year.")
        
        # Decode the VIN to verify if the model and make matches the one from the vin

        url = 'https://vpic.nhtsa.dot.gov/api/vehicles/decodevin/' + vin +'?format=json'  # Replace with your API endpoint URL

        # Make a GET request
        response = requests.get(url)
        
        # Check the response status code
        if response.status_code == 200:
            # Request was successful
            data = response.json() # Parse the response JSON data
            results = data['Results']
            if results[4]['Value'][0] == '0':
                if results[7]['Value'].capitalize() != self.instance.make.capitalize():
                    raise serializers.ValidationError("Make does not match the VIN make")
                if results[9]['Value'].capitalize() != self.instance.model.capitalize():
                    raise serializers.ValidationError("Model does not match the VIN model")
                if int(results[10]['Value']) != int(year):
                    raise serializers.ValidationError("Year does not match the VIN year")
            else:
                raise serializers.ValidationError("Invalid VIN provided.")
        else:
            raise serializers.ValidationError(f"Request failed with status code: {response.status_code}")
        return vin
class Fix_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Fix
        fields = ['user_and_car_id', 'due_date', 'description']