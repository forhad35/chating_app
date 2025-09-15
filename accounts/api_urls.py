from django.urls import path
from .api_views import RegisterAPI, LoginAPI, UserAPI

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='api-register'),
    path('login/', LoginAPI.as_view(), name='api-login'),
    path('user/', UserAPI.as_view(), name='api-user'),
]
