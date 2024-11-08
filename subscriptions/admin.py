from django.contrib import admin
from .models import Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'notification_period', 'next_notification', 'last_status')
    list_filter = ('notification_period',)
    search_fields = ('user__username', 'city__name')