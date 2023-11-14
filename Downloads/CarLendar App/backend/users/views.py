from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from firebase_admin import auth, firestore
from .authentication import is_username_unique, verify_firebase_token, send_email
class SignUp(APIView): 
    def post(self, request):
        data = request.data
        # Validate user data
        if 'username' not in data or 'password' not in data or 'email' not in data:
            return Response({'message': 'Incomplete data'}, status=status.HTTP_400_BAD_REQUEST)
        username = data['username']
        if not is_username_unique(username):
            return Response({'message': 'username already exists'}, status=status.HTTP_409_CONFLICT)
        
        email = data['email']
        password = data['password']
        try:
            #Does the firebase authentication sign up:
            user = auth.create_user(
                email=email,
                password=password,
                email_verified=False,
            )
            #generating email verification link
            link = auth.generate_email_verification_link(user.email)
            print(link)
            #Sending email:
            #send_email(link, email, username)

            #Stores the user in firestore
            firestore_db = firestore.client()

            user_data = {
                "username": username,
                "email": email
            }
            # Add user data to Firestore with UID as the document ID
            user_ref = firestore_db.collection("users").document(user.uid)
            user_ref.set(user_data)
            return Response({"success": True, "message": "User signed up successfully"}, status=status.HTTP_201_CREATED)
        except auth.EmailAlreadyExistsError:
            # Email is already registered
            return Response({'success': False, 'message': 'Email is already registered'}, status=status.HTTP_409_CONFLICT)
        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

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
    def patch(self, request):
        # Assuming the frontend sends the token in the Authorization header
        authorization_header = request.headers.get('Authorization', '')
        id_token = authorization_header.split('Bearer ')[-1]
        data = request.data

        if 'email' not in data:
            return Response({'message': 'Email not provided'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        new_email = data['email']

        try:
            # Verify the Firebase token
            uid = verify_firebase_token(id_token)

            if uid[0] == None:
                return Response({'status': 'error', 'message': uid[1]}, status=status.HTTP_401_UNAUTHORIZED)

            # Updating the email of the user on Firebase Authentication
            updated_user = auth.update_user(uid, email=new_email)

            # Initialize Firestore
            firestore_db = firestore.client()

            # Reference to the user's document
            user_ref = firestore_db.collection("users").document(uid)

            # Update the email field in Firestore
            user_ref.update({"email": updated_user.email})

            return Response({'status': 'success'}, status=status.HTTP_200_OK)

        except Exception as e:
            # Handle any errors
            return Response({'status': 'error', 'message': f"Error updating Firestore email: {e}"}, status=status.HTTP_304_NOT_MODIFIED)
"""Update the username
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
"""
"""Updating the password
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
"""        
"""
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
"""
"""Update the profile picture
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
"""
GetProfileData (GET): It returns the data of the user_id provided by the client
Parameters: The authorized token and user_id
Returns: Response with HTTP Status, the token, and data : {user_id, username, biography, profile picture}

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
"""
ResetPassword: 
"""
