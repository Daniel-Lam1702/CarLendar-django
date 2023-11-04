from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from django.db.utils import IntegrityError
from .serializers import PostSerializer
from .models import Car
from rest_framework.serializers import ValidationError
# Create your views here.

"""
Create a post for a car community (POST).
It must have usercar_id to get the car_id and user_id and create a post for the car community (POST)
Parameters:
    -Authorization: token
    -usercar_id -> car_id (Community) and user_id (Author)
Returns:
    -Token
    -HTTP Status
"""

"""
Get posts per page. It gets an integer parameter page (n >= 0) that will return the elements n*3 to n*3+3 (GET) 
Parameters:
    -Page
    -Authorization: token
    -usercar_id -> car_id 
Returns:
    -Three posts or less: "posts": [posts]
    -token
    -HTTP Response Status
"""

"""
Delete the post (DELETE). The user requesting the deletion of a post has to match the user_id of the author who posted the post.
Parameters:
    -post_id
    -Authorization: token
    -usercar_id -> user_id == post.author
Return:
    -token
    -HTTP Response status
"""

"""
Update the post (PUT). The user requesting the deletion of a post has to match the user_id of the author who posted the post.
Parameters:
    -post_id
    -Authorization: token
    -usercar_id -> user_id == post.author
Return:
    -token
    -HTTP Response status
"""
