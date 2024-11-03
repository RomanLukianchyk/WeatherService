from rest_framework import serializers
from subscriptions.models import Subscription
from weather.models import City


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name']


class SubscriptionSerializer(serializers.ModelSerializer):
    city = CitySerializer()  # Включает данные о городе
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Subscription
        fields = ['id', 'user', 'city', 'notification_period', 'subscribed_at', 'next_notification']
        read_only_fields = ['user', 'subscribed_at', 'next_notification']
