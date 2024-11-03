from django.db import models
from django.contrib.auth.models import User
from weather.models import City
from django.utils import timezone
from datetime import timedelta


class Subscription(models.Model):
    PERIOD_CHOICES = [
        (1, '1 minute'),
        (60, '1 hour'),
        (180, '3 hours'),
        (360, '6 hours'),
        (720, '12 hours'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='subscriptions')
    notification_period = models.IntegerField(choices=PERIOD_CHOICES, default=60)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    next_notification = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.city.name} ({self.get_notification_period_display()})"

    def update_next_notification(self):
        self.next_notification = timezone.now() + timedelta(minutes=self.notification_period)
        self.save()
