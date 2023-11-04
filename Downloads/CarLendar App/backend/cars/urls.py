from django.urls import path
from . import views
urlpatterns = [
    path('create-or-find-car/', views.CreateOrGetCar.as_view(), name='create_or_find_car'),
]