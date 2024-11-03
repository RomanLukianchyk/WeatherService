from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('', lambda request: render(request, 'home.html'), name='home'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('cities/', include('weather.urls')),
    path('subscriptions/', include('subscriptions.urls')),
    path('api/', include('subscriptions.urls')),
]
