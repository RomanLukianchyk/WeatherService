from datetime import timedelta

from django.utils import timezone

from repositories.city_repository import CityRepository
from repositories.subscription_repository import SubscriptionRepository
from subscriptions.models import Subscription
from django.contrib.auth.models import User
from typing import List, Dict


class SubscriptionService:
    @staticmethod
    def get_user_subscribed_city_ids(user: User) -> Dict[str, int]:
        subscriptions = Subscription.objects.filter(user=user)
        return {sub.city.name: sub.id for sub in subscriptions}

    @staticmethod
    def get_user_subscriptions(user: User) -> List[Subscription]:
        return SubscriptionRepository.get_user_subscriptions(user)

    @staticmethod
    def get_subscription_by_id(subscription_id: int, user: User):

        return SubscriptionRepository.get_subscription_by_id(subscription_id, user)

    @staticmethod
    def create_subscription(user, city, notification_period):
        subscription = SubscriptionRepository.create_subscription(user, city, notification_period)
        SubscriptionService.update_next_notification(subscription)
        return subscription

    @staticmethod
    def update_subscription(subscription_id: int, user: User, notification_period: int):
        subscription = SubscriptionRepository.get_subscription_by_id(subscription_id, user)
        if not subscription:
            raise ValueError("Subscription not found")

        SubscriptionRepository.update_subscription(subscription, notification_period)
        SubscriptionService.update_next_notification()

    @staticmethod
    def update_next_notification(subscription):
        subscription.next_notification = timezone.now() + timedelta(minutes=subscription.notification_period)
        subscription.save()

    @staticmethod
    def delete_subscription(subscription_id: int, user: User):
        subscription = SubscriptionRepository.get_subscription_by_id(subscription_id, user)
        if subscription:
            SubscriptionRepository.delete_subscription(subscription)