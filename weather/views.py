import requests
from typing import Any, Dict, List, Iterable
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.core.cache import cache
from django.http import HttpRequest, HttpResponse
from django.db.models.query import QuerySet

from subscriptions.models import Subscription
from weather.forms import CityForm
from weather.models import City

API_KEY = "14adfd6ef710a34827c37d1596426dfe"


def get_weather_data(city_name: str) -> Dict[str, Any]:
    cache_key = city_name.replace(" ", "_")
    cached_data = cache.get(cache_key)
    if cached_data:
        return cached_data

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        data = {'cod': 'error', 'message': str(e)}

    # Сохраняем данные в кеш на 10 минут
    cache.set(cache_key, data, timeout=600)
    return data


def get_weather_for_cities(cities: Iterable[City], user_subscribed_cities: Dict[str, int]) -> List[Dict[str, Any]]:
    weather_list = []
    for city in cities:
        city_weather = get_weather_data(city.name)
        cod = city_weather.get("cod")
        if cod == 200:
            main = city_weather.get('main', {})
            weather_info = city_weather.get('weather', [{}])[0]
            weather_description = weather_info.get('description', '')
            icon = weather_info.get('icon', '')
            temperature = main.get('temp')
        else:
            weather_description = 'City not found'
            icon = ''
            temperature = None

        weather = {
            'city': city.name,
            'temperature': temperature,
            'description': weather_description,
            'icon': icon,
            'subscription_id': user_subscribed_cities.get(city.name),
            'city_id': city.id,
        }
        weather_list.append(weather)
    return weather_list


def city_weather(request: HttpRequest) -> HttpResponse:
    query = request.GET.get('q')
    all_cities = City.objects.filter(name__icontains=query) if query else City.objects.all()

    user_added_cities = all_cities.filter(is_user_added=True)
    popular_cities = all_cities.filter(is_user_added=False)

    user_subscriptions = Subscription.objects.filter(user=request.user)
    user_subscribed_cities = {sub.city.name: sub.id for sub in user_subscriptions}

    user_added_weather = get_weather_for_cities(user_added_cities, user_subscribed_cities)
    popular_weather = get_weather_for_cities(popular_cities, user_subscribed_cities)

    form = CityForm()
    context = {
        'user_added_weather': user_added_weather,
        'popular_weather': popular_weather,
        'form': form,
        'query': query,
    }
    return render(request, 'weather/city_weather.html', context)


@require_POST
def delete_city(request: HttpRequest, city_name: str) -> HttpResponse:
    city = get_object_or_404(City, name=city_name)
    city.delete()
    return redirect('city_weather')


def add_city(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            city_name = form.cleaned_data['name']
            city, created = City.objects.get_or_create(name=city_name)
            if created:
                city.is_user_added = True
                city.save()
            return redirect('city_weather')
    return redirect('city_weather')
