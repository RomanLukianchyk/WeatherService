from django.urls import path
from users import views
from users.views import secured_data_view


urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('generate-token/', views.generate_token_view, name='generate_token'),
    path('get-jwt-token/', views.get_jwt_token, name='get_jwt_token'),
    path('secured-data/', secured_data_view, name='secured_data'),
]
