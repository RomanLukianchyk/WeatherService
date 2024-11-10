from django.core.management.base import BaseCommand
from django.utils import timezone
from subscriptions.models import Subscription
from notifications.services.notification_service import NotificationService


class Command(BaseCommand):
    help = 'Send weather notifications to subscribed users based on individual schedules'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        subscriptions = Subscription.objects.filter(next_notification__lte=now)

        user_notifications = NotificationService.prepare_user_notifications(subscriptions)
        NotificationService.send_email_notifications(user_notifications)
        NotificationService.send_webhook_notifications(user_notifications)

        self.stdout.write(self.style.SUCCESS("Notifications sent successfully"))
