import logging
import os
from typing import Dict, Any
from django.core.cache import cache
import requests
from environ import environ
from settings import BASE_DIR

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


class WeatherService:
    API_KEY = env('WEATHER_API_KEY')

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

