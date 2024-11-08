from django.db import models
from django.contrib.auth.models import User

from weatherproject import settings
from weather.models import City
from django.utils import timezone
from datetime import timedelta


class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscriptions')
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='subscriptions')
    notification_period = models.IntegerField(default=60)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    next_notification = models.DateTimeField(default=timezone.now)
    last_status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return f"{self.user.username} - {self.city.name} ({self.notification_period} minutes)"


