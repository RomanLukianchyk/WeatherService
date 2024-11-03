from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from subscriptions.models import Subscription
from subscriptions.forms import SubscriptionForm
from django.contrib.auth.decorators import login_required

from subscriptions.serializers import CitySerializer, SubscriptionSerializer
from weather.models import City


@login_required
def subscription_list(request):
    subscriptions = Subscription.objects.filter(user=request.user)
    return render(request, 'subscriptions/subscription_list.html', {'subscriptions': subscriptions})


@login_required
def add_subscription(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            subscription = form.save(commit=False)
            subscription.user = request.user
            subscription.save()
            return redirect('subscription_list')
    else:
        form = SubscriptionForm()
    return render(request, 'subscriptions/add_subscription.html', {'form': form})


@login_required
def edit_subscription(request, subscription_id):
    subscription = get_object_or_404(Subscription, id=subscription_id, user=request.user)
    if request.method == 'POST':
        form = SubscriptionForm(request.POST, instance=subscription)
        if form.is_valid():
            form.save()
            return redirect('subscription_list')
    else:
        form = SubscriptionForm(instance=subscription)
    return render(request, 'subscriptions/edit_subscription.html', {'form': form})


@login_required
def delete_subscription(request, subscription_id):
    subscription = get_object_or_404(Subscription, id=subscription_id, user=request.user)
    if request.method == 'POST':
        subscription.delete()
        return redirect('subscription_list')
    return render(request, 'subscriptions/delete_subscription.html', {'subscription': subscription})


@login_required
def add_subscription_from_city(request, city_id):
    city = get_object_or_404(City, id=city_id)
    Subscription.objects.create(user=request.user, city=city, notification_period=3)
    return redirect('subscription_list')


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [IsAuthenticated]


class SubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)

    def perform_create(self, serializer):

        serializer.save(user=self.request.user)