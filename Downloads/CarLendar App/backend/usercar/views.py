from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from django.db.utils import IntegrityError
from .serializers import User_Car_Serializer
from .models import User_and_Car, Fix

#Create a car relation with a user (POST): Parameters: {user_id, car_id, vin, year, mileage} 
# This method is called whenever a user registers their car
class CreateUserCar(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        try:
            user_id = request.user.id  # Retrieve the user's ID from the token
            data = request.data
            car_id = data.get('car_id')
            vin = data.get('vin')
            
            # Now, you can use the 'user_id' in your logic as needed.
            if User_and_Car.objects.filter(car_id=car_id, user_id=user_id, vin=vin).exists():
                return Response({'message': 'Car is already registered'}, status=status.HTTP_400_BAD_REQUEST)
            serializer = User_Car_Serializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'User car created successfully', 'data': serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            return Response({'message': 'Database integrity error'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#Generate the Fixes for a specific caruser (POST) Web Scraping

#Get the Fixes for a specific user car (GET)

#Get the car information from the cars of the user (GET)
class GetUserCar(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        try:
            user_id = request.user.id
            cars = User_and_Car.objects.filter(user_id=user_id).all()
            if cars:
                return Response({'message': 'Cars found for the user', 'data':[User_Car_Serializer(car).data for car in cars]}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': 'Cars not found'}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError:
            return Response({'message': 'Database integrity error'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

