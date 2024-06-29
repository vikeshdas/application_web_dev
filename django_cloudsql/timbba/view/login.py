from django.views import View
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, get_user_model
import json
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
import logging

User = get_user_model()

logger = logging.getLogger(__name__)

class LoginView(APIView):
    """
        View class to check a user is authenticated or not.
    """
    permission_classes = [AllowAny]

    def put(self, request):
        """
        Check username and passwrid is matching in databsae or not.If user is authenticated it will return 
        a token.

        Args:
            HttpRequest :Contains username and password in request body.

        Returns:
            JsonResponse:return JSON contains referesh token. 
        """
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
        except (json.JSONDecodeError, TypeError, KeyError):
            return JsonResponse({'error': 'Invalid input'}, status=400)

        if not username or not password:
            return JsonResponse({'error': 'Username and password are required'}, status=400)

        try:
            user = User.objects.get(username=username)
            logger.debug(f"FETCH USER: {user}")
        except User.DoesNotExist:
            return JsonResponse({'error': 'Invalid username'}, status=401)


        is_authUser = authenticate(request, username=username, password=password)
        
        if is_authUser:
            login(request, is_authUser)
            refresh = RefreshToken.for_user(is_authUser)
            return JsonResponse({'message': 'Logged in successfully', 'refresh': str(refresh),'access': str(refresh.access_token)}, status=200)
        else:
            return JsonResponse({'error': 'Invalid password'}, status=401)