from django.db import models
from users.models import User
from cars.models import Car
# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    body =  models.TextField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    car_id = models.ForeignKey(Car, on_delete=models.CASCADE)
    created_at = models.DateTimeField()

    class Meta:
        # Define an index on the date_field field in descending order
        indexes = [
            models.Index(fields=['created_at'], name='idx_date_field_desc'),
        ]