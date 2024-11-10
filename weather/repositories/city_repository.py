from subscriptions.models import Subscription
from weather.models import City
from typing import List, Optional


class CityRepository:
    @staticmethod
    def get_all_cities() -> List[City]:
        return City.objects.all()

    @staticmethod
    def get_city_by_name(name: str) -> Optional[City]:
        return City.objects.filter(name=name).first()

    @staticmethod
    def get_user_subscribed_cities(user):
        return Subscription.objects.filter(user=user).values_list('city', flat=True)

    @staticmethod
    def create_city(name: str) -> City:
        city, created = City.objects.get_or_create(name=name, defaults={'is_user_added': True})
        return city

    @staticmethod
    def get_city_by_id(city_id):
        try:
            return City.objects.get(id=city_id)
        except City.DoesNotExist:
            return None

    @staticmethod
    def delete_city(city: City):
        city.delete()

    @staticmethod
    def get_or_create_city(name):
        city, created = City.objects.get_or_create(name=name)
        return city, created

    @staticmethod
    def search_cities(query=None):
        if query:
            return City.objects.filter(name__icontains=query)
        return City.objects.all()
