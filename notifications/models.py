from django.db import models
from django.contrib.auth.models import User
from subscriptions.models import Subscription


class NotificationLog(models.Model):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    last_notified = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.subscription.city} to {self.subscription.user.email}"
