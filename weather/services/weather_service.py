
from typing import Tuple, Any
from django.conf import settings
import requests
from django.core.cache import cache
import logging

from weather.repositories.city_repository import CityRepository


class WeatherService:
    API_KEY = settings.WEATHER_API_KEY

    @staticmethod
    def get_weather_data(city_name: str) -> dict:
        cache_key = f"weather_data_{city_name.replace(' ', '_')}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data

        url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={WeatherService.API_KEY}&units=metric"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            cache.set(cache_key, data, timeout=600)
            return data
        except requests.RequestException as e:
            logging.error(f"Error fetching weather data for {city_name}: {e}")
            return {
                "city": city_name,
                "error": "Unable to fetch data",
                "temperature": None,
                "description": "No data"
            }

    @staticmethod
    def add_city(name: str) -> Tuple[Any, bool]:
        city, created = CityRepository.get_or_create_city(name)
        if created:
            city.is_user_added = True
            city.save()
        return city, created
