import logging
import requests
from django.conf import settings
from django.core.mail import send_mail
from collections import defaultdict
from weather.services.weather_service import WeatherService


class NotificationService:

    @staticmethod
    def prepare_user_notifications(subscriptions):
        user_notifications = defaultdict(list)
        for subscription in subscriptions:
            city_name = subscription.city.name
            weather_data = WeatherService.get_weather_data(city_name)

            city_info = {
                'city': city_name,
                'temperature': weather_data.get('main', {}).get('temp'),
                'description': weather_data.get('weather', [{}])[0].get('description')
            }

            user_notifications[subscription].append(city_info)

            subscription.update_next_notification()

        return user_notifications

    @staticmethod
    def send_email_notifications(user_notifications):
        for subscription, notifications in user_notifications.items():
            user = subscription.user
            subject = f"Weather Update for {subscription.city.name}"
            message = "\n\n".join(
                [f"City: {info['city']}\nTemperature: {info['temperature']}°C\nDescription: {info['description']}"
                 for info in notifications]
            )

            try:
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                )
                logging.info(f"Email sent to {user.email}")
            except Exception as e:
                logging.error(f"Failed to send email to {user.email}: {e}")

    @staticmethod
    def send_webhook_notifications(user_notifications):
        for subscription, notifications in user_notifications.items():
            webhook_url = subscription.webhook_url
            if webhook_url:
                payload = {
                    'user': subscription.user.username,
                    'notifications': notifications,
                }
                try:
                    requests.post(webhook_url, json=payload)
                except requests.RequestException as e:
                    print(f"Error sending webhook for {subscription}: {e}")
