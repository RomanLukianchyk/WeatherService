from django.urls import path, include
from rest_framework.routers import DefaultRouter
from subscriptions import views
from subscriptions.views import CityViewSet, SubscriptionViewSet

#  API
router = DefaultRouter()
router.register(r'cities', CityViewSet, basename='city')
router.register(r'subscriptions', SubscriptionViewSet, basename='subscription')

# Основные URL-маршруты
urlpatterns = [

    path('api/', include(router.urls)),

    path('', views.subscription_list, name='subscription_list'),
    path('add/', views.add_subscription, name='add_subscription'),
    path('add_from_city/<int:city_id>/', views.add_subscription_from_city, name='add_subscription_from_city'),
    path('edit/<int:subscription_id>/', views.edit_subscription, name='edit_subscription'),
    path('delete/<int:subscription_id>/', views.delete_subscription, name='delete_subscription'),
]
