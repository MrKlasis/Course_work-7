from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from app_users.models import User


class RegisterUserSerializer(serializers.ModelSerializer):

    password_again = serializers.CharField(
        max_length=128,
        label=_("Password (again)"),
        write_only=True
    )

    def save(self, *args, **kwargs):
        user = User(
            email=self.validated_data['email'],
            first_name=self.validated_data.get('first_name') if self.validated_data.get('first_name') else "",
            last_name=self.validated_data.get('last_name') if self.validated_data.get('last_name') else "",
            telegram_id=self.validated_data.get('telegram_id') if self.validated_data.get('telegram_id') else "",
        )

        password = self.validated_data['password']
        password_again = self.validated_data['password_again']

        if password != password_again:
            raise serializers.ValidationError({'detail': "Введенные пароли не совпадают"})

        user.set_password(password)
        user.save()
        return user

    class Meta:
        model = User
        fields = ('email', 'password', 'password_again', 'first_name', 'last_name', 'telegram_id')
        extra_kwargs = {
            'password': {'write_only': True},
        }
