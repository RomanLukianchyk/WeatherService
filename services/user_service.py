from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpRequest
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from users.forms import UserRegisterForm
from django.contrib.auth.forms import AuthenticationForm


class UserService:
    @staticmethod
    def register_user(request: HttpRequest) -> JsonResponse:
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return JsonResponse({
                    'message': 'Registration successful.',
                    'user_id': user.id,
                    'username': user.username,
                }, status=status.HTTP_201_CREATED)
            else:
                return JsonResponse({
                    'errors': form.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'error': 'Invalid request method.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @staticmethod
    def login_user(request: HttpRequest) -> JsonResponse:
        if request.method == 'POST':
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                return JsonResponse({
                    'message': 'Login successful.',
                    'user_id': user.id,
                    'username': user.username,
                }, status=status.HTTP_200_OK)
            else:
                return JsonResponse({
                    'errors': form.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'error': 'Invalid request method.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @staticmethod
    def logout_user(request: HttpRequest) -> JsonResponse:
        logout(request)
        return JsonResponse({
            'message': "You have been logged out successfully."
        }, status=status.HTTP_200_OK)

    @staticmethod
    def generate_jwt_token(user: User) -> JsonResponse:
        refresh = RefreshToken.for_user(user)
        return JsonResponse({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)

    @staticmethod
    def update_webhook_url(user, webhook_url):
        if not webhook_url:
            raise ValidationError("Webhook URL is required.")

        user.webhook_url = webhook_url
        user.save()
        return {'message': 'Webhook URL updated successfully'}

    @staticmethod
    def get_tokens_for_user(user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
