from django.urls import path
from users.views import register, login_view, logout_view, generate_token, secured_data_view, set_webhook

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('generate_token/', generate_token, name='generate_token'),
    path('secured_data/', secured_data_view, name='secured_data'),
    path('set_webhook/', set_webhook, name='set_webhook'),
]