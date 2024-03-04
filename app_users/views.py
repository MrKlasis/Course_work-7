from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from app_users.models import User
from app_users.serializers import RegisterUserSerializer


class RegisterUserAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer
    permission_classes = [AllowAny]
