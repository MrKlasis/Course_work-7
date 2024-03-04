from django.contrib.auth.models import AbstractUser
from django.db import models

NULL = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='Email')

    phone_number = models.CharField(max_length=35, verbose_name='номер телефона', **NULL)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULL)
    telegram_id = models.CharField(max_length=10, verbose_name='ID телеграмм чата')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
