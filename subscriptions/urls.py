from django.urls import path
from subscriptions.views import add_subscription, update_subscription, delete_subscription

urlpatterns = [
    path('add/', add_subscription, name='add_subscription'),
    path('<int:subscription_id>/update/', update_subscription, name='update_subscription'),
    path('<int:subscription_id>/delete/', delete_subscription, name='delete_subscription'),
]