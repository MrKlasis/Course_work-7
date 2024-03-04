from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from app_users.apps import AppUsersConfig
from app_users.views import RegisterUserAPIView

app_name = AppUsersConfig.name

urlpatterns = [
    path('register/', RegisterUserAPIView.as_view(), name="register"),
    path('token/', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('token/refresh/', TokenRefreshView.as_view(), name="token_refresh"),
]
