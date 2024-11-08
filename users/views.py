from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

from services.user_service import UserService


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    response = UserService.register_user(request)
    if isinstance(response, dict):
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    return Response({'message': 'Registration successful'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    response = UserService.login_user(request)
    if isinstance(response, dict):
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    response = UserService.logout_user(request)
    return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def generate_token(request):
    response = UserService.generate_jwt_token(request.user)
    return Response(response)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def generate_token_view(request):
    user = request.user
    refresh = RefreshToken.for_user(user)

    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def set_webhook(request):
    user = request.user
    webhook_url = request.data.get('webhook_url')

    try:
        result = UserService.update_webhook_url(user, webhook_url)
        return Response(result, status=status.HTTP_200_OK)
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def secured_data_view(request):
    data = {
        'message': 'This is a secured data available only for authenticated users.'
    }
    return Response(data)
