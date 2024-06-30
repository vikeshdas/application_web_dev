"""
This module defines a view for user login using Django and Django
REST framework.It provides a class-based view that handles user 
authentication and returns a JSON response containing JWT tokens
on successful login

Classes:
LoginView: An API view class that verifies user credentials and
returns JWT tokens.

"""
import json
import logging

from django.contrib.auth import authenticate, get_user_model, login
from django.http import JsonResponse, HttpRequest
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

logger = logging.getLogger(__name__)


class LoginView(APIView):
    """
    View class to check a user is authenticated or not.
    """

    permission_classes = [AllowAny]

    def put(self, request: HttpRequest) -> JsonResponse:
        """
        Check username and passwrid is matching in databsae or not.If user is
        authenticated it will return a token.

        Args:
            HttpRequest :Contains username and password in request body.

        Returns:
            JsonResponse:return JSON contains referesh token.
        """
        try:
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")
        except (json.JSONDecodeError, TypeError, KeyError):
            return JsonResponse({"error": "Invalid input"}, status=400)

        if not username or not password:
            return JsonResponse(
                {"error": "Username and password are required"}, status=400
            )

        try:
            user = User.objects.get(username=username)
            logger.debug("FETCH USER: %s", user)
        except User.DoesNotExist:
            return JsonResponse({"error": "Invalid username"}, status=401)

        is_auth_user = authenticate(request, username=username, password=password)

        if is_auth_user:
            login(request, is_auth_user)
            refresh = RefreshToken.for_user(is_auth_user)
            return JsonResponse(
                {
                    "message": "Logged in successfully",
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=200,
            )
        
        return JsonResponse({"error": "Invalid password"}, status=401)
