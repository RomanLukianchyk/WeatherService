from django.contrib import admin
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'webhook_url')
    search_fields = ('username', 'email')
    list_filter = ('is_active', 'is_staff')