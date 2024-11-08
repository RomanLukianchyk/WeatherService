from subscriptions.models import Subscription
from django.contrib.auth.models import User
from weather.models import City
from django.utils import timezone
from typing import List, Optional


class SubscriptionRepository:
    @staticmethod
    def get_user_subscriptions(user: User) -> List[Subscription]:
        return Subscription.objects.filter(user=user)

    @staticmethod
    def get_subscription_by_id(subscription_id: int, user: User):
        return Subscription.objects.filter(id=subscription_id, user=user).first()

    @staticmethod
    def create_subscription(user: User, city: City, notification_period: int) -> Subscription:
        subscription = Subscription(user=user, city=city, notification_period=notification_period)
        subscription.next_notification = timezone.now()
        subscription.save()
        return subscription

    @staticmethod
    def update_subscription(subscription: Subscription, notification_period: int):
        subscription.notification_period = notification_period
        subscription.next_notification = timezone.now()
        subscription.save()

    @staticmethod
    def delete_subscription(subscription: Subscription):
        subscription.delete()