from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from weather.services.weather_service import WeatherService
from weather.repositories.city_repository import CityRepository


class CityViewSet(viewsets.ViewSet):
    def list(self, request):
        query = request.query_params.get('q')
        weather_data = WeatherService.get_weather_for_cities(query)
        return Response(weather_data)

    @action(detail=True, methods=['post'])
    def add_city(self, request):
        city_name = request.data.get('name')
        if not city_name:
            return Response({"error": "City name is required."}, status=status.HTTP_400_BAD_REQUEST)

        city, created = WeatherService.add_city(city_name)

        if created:
            return Response({"message": f"{city_name} City add."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": f"{city_name} already exists."}, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        city = CityRepository.get_city_by_id(pk)
        if city:
            return Response({'city': city.name})
        return Response({'error': 'City not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk=None):
        city = CityRepository.get_city_by_id(pk)
        if city:
            city_name = city.name
            CityRepository.delete_city(city)
            return Response({'message': f'City {city_name} has been deleted successfully.'}, status=status.HTTP_200_OK)
        return Response({'error': 'City not found'}, status=status.HTTP_404_NOT_FOUND)