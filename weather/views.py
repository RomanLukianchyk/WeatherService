from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from services.weather_service import WeatherService
from repositories.city_repository import CityRepository


class CityViewSet(viewsets.ViewSet):
    def list(self, request):
        query = request.query_params.get('q')
        weather_data = WeatherService.get_weather_for_cities(query)
        return Response(weather_data)

    @action(detail=True, methods=['post'])
    def add_city(self, request):
        name = request.data.get('name')
        city = CityRepository.create_city(name)
        return Response({'city': city.name}, status=status.HTTP_201_CREATED)

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