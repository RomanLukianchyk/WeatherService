import requests
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from subscriptions.models import Subscription
from weather.views import get_weather_data
from collections import defaultdict


class Command(BaseCommand):
    help = 'Send weather notifications to subscribed users based on individual schedules'

    def handle(self, *args, **kwargs):
        now = timezone.now()

        # Собираем уведомления для отправки
        user_notifications = defaultdict(list)
        subscriptions = Subscription.objects.filter(next_notification__lte=now)

        for subscription in subscriptions:
            city_name = subscription.city.name
            weather_data = get_weather_data(city_name)

            # Формируем текст уведомления для города
            city_info = (
                f"City: {city_name}\n"
                f"Temperature: {weather_data.get('main', {}).get('temp')}°C\n"
                f"Description: {weather_data.get('weather', [{}])[0].get('description')}\n"
            )

            # Добавляем уведомление для пользователя
            user_notifications[subscription.user.email].append(city_info)

            # Обновляем время следующего уведомления для подписки
            subscription.update_next_notification()

        # Отправка email для каждого пользователя
        for user_email, notifications in user_notifications.items():
            subject = "Weather Update for Your Subscribed Cities"
            message = "\n\n".join(notifications)
            from_email = '19arrow19@gmail.com'

            # Отправляем одно email-сообщение с информацией по всем городам
            send_mail(
                subject,
                message,
                from_email,
                [user_email],
                fail_silently=False,
            )

            # Дополнительно отправляем webhook для каждого пользователя
            webhook_url = "https://webhook.site/f49baac4-5baa-47e1-91ad-61dc1b12eaf6"
            payload = {
                'user': user_email,
                'notifications': notifications,
            }
            requests.post(webhook_url, json=payload)

        self.stdout.write(self.style.SUCCESS("Notifications sent successfully"))
