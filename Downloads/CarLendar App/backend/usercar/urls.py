from django.urls import path
from . import views
urlpatterns = [
    path('create-user-car/', views.CreateUserCar.as_view(), name = 'create-user-car'),
    path('get-user-car/', views.GetUserCar.as_view(), name = 'get-user-car'),
]