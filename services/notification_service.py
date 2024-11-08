import logging
import os

import requests
from django.core.mail import send_mail
from collections import defaultdict
from django.utils import timezone
from environ import environ

from services.weather_service import WeatherService
from settings import BASE_DIR

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


class NotificationService:
    @staticmethod
    def prepare_user_notifications(subscriptions):
        user_notifications = defaultdict(list)
        for subscription in subscriptions:
            city_weather = WeatherService.get_weather_data(subscription.city.name)
            city_info = {
                "city": subscription.city.name,
                "temperature": f"{city_weather.get('main', {}).get('temp')}°C",
                "description": city_weather.get('weather', [{}])[0].get('description')
            }
            user_notifications[subscription.user].append(city_info)
            subscription.update_next_notification()
        return user_notifications

    @staticmethod
    def send_email_notifications(user_notifications):
        for user, notifications in user_notifications.items():
            subject = "Weather Update for Your Subscribed Cities"
            message = "\n\n".join(
                [f"City: {city['city']}\nTemperature: {city['temperature']}\nDescription: {city['description']}"
                 for city in notifications]
            )
            try:
                send_mail(
                    subject,
                    message,
                    env('EMAIL_HOST_USER'),
                    [user.email],
                    fail_silently=False,
                )
                logging.info(f"Email sent to {user.email}")
            except Exception as e:
                logging.error(f"Failed to send email to {user.email}: {e}")

    @staticmethod
    def send_webhook_notifications(user_notifications):
        for user, notifications in user_notifications.items():
            if user.webhook_url:
                payload = {
                    'user': user.email,
                    'notifications': notifications
                }
                try:
                    response = requests.post(user.webhook_url, json=payload)
                    response.raise_for_status()
                    logging.info(f"Webhook sent to {user.webhook_url}")
                except requests.RequestException as e:
                    logging.error(f"Failed to send webhook for {user.email} to {user.webhook_url}: {e}")
