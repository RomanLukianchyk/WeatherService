from django.urls import path
from weather.views import CityViewSet

city_list = CityViewSet.as_view({'get': 'list', 'post': 'add_city'})
city_detail = CityViewSet.as_view({'get': 'retrieve', 'delete': 'delete'})

urlpatterns = [
    path('cities/', city_list, name='city-list'),
    path('cities/<int:pk>/', city_detail, name='city-detail'),
]