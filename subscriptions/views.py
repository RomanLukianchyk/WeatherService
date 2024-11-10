import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from subscriptions.services.subscription_service import SubscriptionService


logger = logging.getLogger(__name__)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_subscription(request):
    user = request.user
    city_name = request.data.get('city_name')
    notification_period = request.data.get('notification_period')
    try:
        subscription = SubscriptionService.create_subscription(user, city_name, notification_period)
        return Response({'message': f'Subscribed to {subscription.city.name}'}, status=status.HTTP_201_CREATED)
    except ValueError as e:
        logger.error(f"Error adding subscription for user {user.username}: {e}")
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_subscription(request, subscription_id):
    user = request.user
    notification_period = request.data.get('notification_period')
    try:
        SubscriptionService.update_subscription(subscription_id, user, notification_period)
        return Response({'message': 'Subscription updated successfully'}, status=status.HTTP_200_OK)
    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_subscription(request, subscription_id):
    user = request.user
    SubscriptionService.delete_subscription(subscription_id, user)
    return Response({'message': 'Subscription deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
