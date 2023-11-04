from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from django.db.utils import IntegrityError
from .serializers import CarSerializer
from .models import Car
from rest_framework.serializers import ValidationError

# It creates a car forum if it doesn't exist. If it already exists, it returns it.
class CreateOrGetCar(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = request.data
            serializer = CarSerializer(data=data)

            if serializer.is_valid():
                make = serializer.validated_data.get("make")
                model = serializer.validated_data.get("model")
                
                record, created = Car.objects.get_or_create(make=make, model=model)

                if created:
                    return Response({'message': 'Car forum created', 'data': CarSerializer(record).data}, status=status.HTTP_201_CREATED)
                else:
                    return Response({'message': 'Car forum found', 'data': CarSerializer(record).data}, status=status.HTTP_202_ACCEPTED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            return Response({'message': 'Database integrity error'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetCar(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            data = request.data
            if "car_id" not in data:
                Response({'message':'car id required'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                car = Car.objects.get(id=data["car_id"])
                serializer = CarSerializer(car)
                return Response({'message':'Car successfully found', 'data': serializer.data}, status=status.HTTP_202_ACCEPTED)
        except Car.DoesNotExist:
            return Response({'message': 'Car not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)   