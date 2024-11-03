from django.urls import path
from . import views

urlpatterns = [
    path('', views.city_weather, name='city_weather'),
    path('delete/<str:city_name>/', views.delete_city, name='delete_city'),
    path('add/', views.add_city, name='add_city'),
]
