from django.shortcuts import render
from django.contrib.auth.hashers import make_password, check_password
from django.db.utils import IntegrityError
from .models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .serializers import UserSerializer
from random import randint
from django.core.mail import EmailMessage

class SignUp(APIView):
    def getOTP(self):
        otp = ""
        for i in range(0, 6):
            otp += str(randint(0,9))
        return otp

    def send_email(self, email, otp):
        subject = 'OTP Email Verification'
        message = 'Hi,\n\n I hope you are having a good day. the otp verification for your CarLendar account is:\n\n' + otp
        from_email = 'CarLendarTesting@gmail.com'  # Sender's email address
        recipient_list = [email]  # List of recipient email addresses
        email = EmailMessage(subject, message, from_email, recipient_list)
        sent = email.send()
        print(sent)
    def post(self, request):
        try:
            
            data = request.data
            # Validate user data
            
            if 'username' not in data or 'password' not in data or 'email' not in data:
                return Response({'message': 'Incomplete data'}, status=status.HTTP_400_BAD_REQUEST)

            email = data['email']
            username = data['username']
            
            # Check if the email already exists in the database
            if User.objects.filter(email=email).exists() and User.objects.get(email=email).is_email_validated:
                return Response({'message': 'Email already exists'}, status=status.HTTP_409_CONFLICT)
            elif User.objects.filter(username=username).exists():
                return Response({'message': 'username already exists'}, status=status.HTTP_409_CONFLICT)
            else:
                user = User()
                user.username = data['username']
                user.password = make_password(data['password'])
                user.email = email
                otp = self.getOTP()
                user.otp = otp
                #Create a otp
                self.send_email(email, otp)
                print(otp)
                user.save()
                return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({'message': 'Database integrity error'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class ActivateUser(APIView):
    def patch(self, request):
        try:
            data = request.data
            if 'otp' not in data or 'email' not in data:
                return Response({'message': 'Incomplete data', 'validated': False}, status=status.HTTP_400_BAD_REQUEST)
            otp = data["otp"]
            email = data["email"]            
            user = User.objects.get(email=email)
            if user:
                if user.is_email_validated:
                    return Response({'message': 'email was already validated', 'validated': False}, status=status.HTTP_409_CONFLICT)
                elif user.otp == otp:
                    user.is_email_validated = True
                    user.save()
                    return Response({'message': 'email successfully validated', 'validated': True}, status=status.HTTP_202_ACCEPTED)
                else:
                    return Response({'message': 'invalid otp', 'validated': False}, status=status.HTTP_409_CONFLICT)
            else:
                return Response({'message': 'User created successfully', 'validated': False}, status=status.HTTP_201_CREATED)  
        except IntegrityError:
            return Response({'message': 'Database integrity error','validated': False}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': 'An error occurred', 'validated': False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class SignIn(APIView):
    def post(self, request):
        try:
            data = request.data
            if 'username' not in data or 'password' not in data:
                return Response({'message': 'Incomplete data'}, status=status.HTTP_400_BAD_REQUEST)
            #Check if the email is not authenticated, the user cannot sign in.
            username = data['username']
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response({'message': 'Invalid username or password'}, status=status.HTTP_404_NOT_FOUND)
            if(not user.is_email_validated):
                return Response({'message': 'Validate the email address'}, status=status.HTTP_404_NOT_FOUND)
            if(check_password(data['password'], user.password)):
                token = AccessToken.for_user(user)
                return JsonResponse({'token': str(token)}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'User and password do not match'}, status=status.HTTP_401_UNAUTHORIZED)
        except IntegrityError:
            return Response({'message': 'Database integrity error'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

"""Verify the email through a generated code in the email"""

"""
PATCH Requests for user_id data with token:
    -Email
    -username
    -password
    -Biography
    -profile Picture
"""
"""Update Email"""
class UpdateEmail(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def patch(self, request):
        try:
            # Retrieve the user
            current_password = request.data["current_password"]
            user = request.user
            email = request.data["email"]
            #Check if the current password matches the current_password requested.
            if check_password(current_password, user.password):
                user.email = email
                #Authenticate new email...
                user.save()
                return Response({'status': 'success'}, status=status.HTTP_200_OK)
            else:
                return Response({'message':'Incorrect current password'}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({'status': 'error', 'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
"""Update the username"""
class UpdateUsername(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def patch(self, request):
        try:
            # Retrieve the user
            current_password = request.data["current_password"]
            user = request.user
            username = request.data["username"]
            #Check if the current password matches the current_password requested.
            if check_password(current_password, user.password):
                user.username = username
                user.save()
                return Response({'status': 'success'}, status=status.HTTP_200_OK)
            else:
                return Response({'message':'Incorrect current password'}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({'status': 'error', 'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
"""Updating the password"""
class UpdatePassword(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def patch(self, request):
        try:
            # Retrieve the user
            current_password = request.data["current_password"]
            new_password = request.data["new_password"]
            user = request.user
            #Check if the current password matches the current_password requested.
            if check_password(current_password, user.password):
                user.password = make_password(new_password)
                user.save()
                return Response({'status': 'success'}, status=status.HTTP_200_OK)
            else:
                return Response({'message':'Incorrect current password'}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({'status': 'error', 'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
"""Update the biography"""
class UpdateBiography(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def patch(self, request):
        try:
            # Retrieve the user
            user = request.user
            biography = request.data["biography"]
            user.biography = biography
            user.save()
            return Response({'status': 'success'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'status': 'error', 'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
"""Update the profile picture"""
class UpdateProfilePicture(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def patch(self, request):
        try:
            # Retrieve the user
            user = request.user
            profile_picture = request.data["profile_picture"]
            user.profile_picture = profile_picture
            user.save()
            return Response({'status': 'success'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'status': 'error', 'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
"""
GetProfileData (GET): It returns the data of the user_id provided by the client
Parameters: The authorized token and user_id
Returns: Response with HTTP Status, the token, and data : {user_id, username, biography, profile picture}
"""
class GetProfileData(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, user_id):
        try:
            # Retrieve the user profile data
            user_profile = User.objects.get(id=user_id)

            # Serialize the user profile data
            serializer = UserSerializer(user_profile)

            # Return the serialized data in the response
            return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'status': 'error', 'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

"""
ResetPassword: 
"""
