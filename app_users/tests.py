from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from app_users.models import User


class UserTest(APITestCase):

    def setUp(self):
        pass

    def test_register(self):
        """ Тестирование регистрации нового пользователя """

        users_count1 = User.objects.all().count()

        data = {
            "email": "user_register_test@sky.pro",
            "password": "123qwe",
            "password_again": "123qwe",
            "first_name": "Test_first_name",
            "last_name": "Test_last_name",
            "telegram_id": "123456789",
        }

        response = self.client.post(
            reverse("app_users:register"),
            data=data
        )

        users_count2 = User.objects.all().count()

        self.assertEquals(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEquals(
            response.json(),
            {
                'email': 'user_register_test@sky.pro',
                'first_name': 'Test_first_name',
                'last_name': 'Test_last_name',
                'telegram_id': "123456789"
            }
        )

        self.assertTrue(
            users_count1 == (users_count2 - 1)
        )

    def test_invalid_password_register(self):
        """
        Тестирование проверки совпадения паролей
        и невозможности создания пользователя в случае ошибки
        """

        users_count1 = User.objects.all().count()

        data = {
            "email": "user_register_test@sky.pro",
            "password": "123qwe",
            "password_again": "qwe123",
            "telegram_id": "123456789",
        }

        response = self.client.post(
            reverse("app_users:register"),
            data=data
        )

        users_count2 = User.objects.all().count()

        self.assertEquals(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEquals(
            response.json(),
            {
                'detail': 'Введенные пароли не совпадают'
            }
        )

        self.assertTrue(
            users_count1 == users_count2
        )
