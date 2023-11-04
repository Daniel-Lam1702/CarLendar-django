# custom_authentication.py

from rest_framework.authentication import TokenAuthentication

class CustomAuthentication(TokenAuthentication):
    def authenticate(self, request):
        # Debugging statement to print the request path and method
        print(f"Request method: {request.method}, Path: {request.path}")

        # Allow unauthenticated access for the SignUp view
        if request.method == 'POST' and (request.path == '/users/signup/' or request.path == '/users/login'):
            return None

        # Debugging statement to indicate when authentication is performed
        print("Authentication is being performed.")

        return super().authenticate(request)