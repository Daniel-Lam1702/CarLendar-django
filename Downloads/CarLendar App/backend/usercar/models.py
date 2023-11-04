from django.db import models
from users.models import User
from cars.models import Car
# Create your models here.
class User_and_Car(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    car_id = models.ForeignKey(Car, on_delete=models.CASCADE)
    vin = models.CharField(max_length=17)
    mileage = models.PositiveIntegerField()
    year = models.PositiveBigIntegerField()

class Fix(models.Model):
    user_and_car_id = models.ForeignKey(User_and_Car, on_delete=models.CASCADE)
    due_date = models.DateField()
    description = models.TextField()
    