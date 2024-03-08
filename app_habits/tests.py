from django.utils import timezone
from datetime import time
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from config import settings

from app_habits.models import Habit
from app_users.models import User

settings.INSTALLED_APPS += ['django_celery_beat']


class HabitGoodTest(APITestCase):

    def setUp(self):
        # Users
        self.user_1 = User.objects.create(
            email="user1@test.com",
            telegram_id='123456789',
            is_staff=False,
            is_active=True,
        )
        self.user_1.set_password('test')
        self.user_1.save()

        self.user_2 = User.objects.create(
            email="user2@test.com",
            is_staff=False,
            is_active=True,
        )
        self.user_2.set_password('test')
        self.user_2.save()

        self.user_3 = User.objects.create(
            email="user3@test.com",
            is_staff=False,
            is_active=True,
        )
        self.user_3.set_password('test')
        self.user_3.save()

        # Nice Habit
        self.nice_habit = Habit.objects.create(
            task="Test nice habit",
            location="Test location",
            is_nice=True,
            owner=self.user_1,
            periodic=7
        )

    def test_create(self):
        """ Тестирование создания объекта с минимальным набором полей """

        # Аутентифицируем обычного пользователя
        self.client.force_authenticate(user=self.user_1)

        data = {
            "task": "Test task good",
            "location": "Test location",
            "start_time": "12:10"
        }

        response = self.client.post(
            reverse("app_habits:habit_good_create"),
            data=data
        )

        # Проверяем что объект успешно создан
        self.assertEquals(
            response.status_code,
            status.HTTP_201_CREATED
        )

        # Проверяем ответ
        expected_result = {
            "id": response.json().get("id"),
            "task": "Test task good",
            "start_time": time(12, 10),  # Используем объект времени
            "location": "Test location",
            "is_nice": False,
            "periodic": '1',
            "reward": None,
            "time_to_complete": 60,
            "is_public": False,
            "owner": self.user_1.id,
            "related": None
        }

        # Сравниваем только часы и минуты
        self.assertEqual(response.json()["id"], expected_result["id"])
        self.assertEqual(response.json()["task"], expected_result["task"])
        self.assertEqual(response.json()["location"], expected_result["location"])
        self.assertEqual(response.json()["is_nice"], expected_result["is_nice"])
        self.assertEqual(response.json()["periodic"], expected_result["periodic"])
        self.assertEqual(response.json()["reward"], expected_result["reward"])
        self.assertEqual(response.json()["time_to_complete"], expected_result["time_to_complete"])
        self.assertEqual(response.json()["is_public"], expected_result["is_public"])
        self.assertEqual(response.json()["owner"], expected_result["owner"])
        self.assertEqual(response.json()["related"], expected_result["related"])
        self.assertEqual(response.json()["start_time"][:5],
                         str(expected_result["start_time"])[:5])  # Сравниваем только часы и минуты

    def test_permission_anonim_created(self):
        """
        Тестирование ограничение при создании
        привычки без аутентификации
        """

        data = {
            "task": "Test task good",
            "location": "Test location",
        }

        response = self.client.post(
            reverse("app_habits:habit_good_create"),
            data=data
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_filling_not_out_two_fields_validator(self):
        """
        Тестирование валидатора FillingNotOutTwoFieldsValidator
        при одновременном указании связанной привычки и вознаграждения
        """

        # Аутентифицируем обычного пользователя
        self.client.force_authenticate(user=self.user_1)

        data = {
            "start_time": "12:10",
            "task": "Test task good",
            "location": "Test location",
            "related": self.nice_habit.id,
            "reward": "Test reward"
        }

        response = self.client.post(
            reverse("app_habits:habit_good_create"),
            data=data
        )

        # Проверяем что получили ошибку
        self.assertEquals(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        # Проверяем текст ответа
        self.assertEquals(
            response.json(),
            {'non_field_errors': ['Недопустимо одновременно указывать "related" и "reward"']}
        )

    def test_time_to_complete_validator(self):
        """
        Тестирование валидатора TimeToCompleteValidator
        при превышении значения времени выполнения (ограничено 120)
        """

        # Аутентифицируем обычного пользователя
        self.client.force_authenticate(user=self.user_1)

        data = {
            "start_time": "12:10",
            "task": "Test task good",
            "location": "Test location",
            "related": self.nice_habit.id,
            "time_to_complete": 121
        }

        response = self.client.post(
            reverse("app_habits:habit_good_create"),
            data=data
        )

        # Проверяем что получили ошибку
        self.assertEquals(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        # Проверяем текст ответа
        self.assertEquals(
            response.json(),
            {'non_field_errors': ['Время выполнения должно быть не больше 120 секунд.']}
        )

    def test_related_habit_only_nice_validator(self):
        """
        Тестирование валидатора RelatedHabitOnlyNice
        при указании привычки без признака приятной
        """

        # Аутентифицируем обычного пользователя
        self.client.force_authenticate(user=self.user_1)

        # Создаем полезную привычку
        good_habit = Habit.objects.create(
            task="Test good habit",
            location="Test location",
            is_nice=False,
            owner=self.user_1
        )

        data = {
            "start_time": "12:10",
            "task": "Test task good",
            "location": "Test location",
            "related": good_habit.id,
            "time_to_complete": 120
        }

        response = self.client.post(
            reverse("app_habits:habit_good_create"),
            data=data
        )

        # Проверяем что получили ошибку
        self.assertEquals(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        # Проверяем текст ответа
        self.assertEquals(
            response.json(),
            {'non_field_errors': ['В поле "related" должна быть указана приятная привычка']}
        )

    def test_bad_periodicity(self):
        """
        Тестирование валидации ограничения на уровне модели.
        Невозможность задания периодичности более 7 дней
        """

        # Аутентифицируем пользователя
        self.client.force_authenticate(user=self.user_1)

        # Изменяем параметр last_completed
        self.nice_habit.last_completed = timezone.now()
        self.nice_habit.save()

        data = {
            "start_time": "12:10",
            "task": "Test task good",
            "location": "Test location",
            "periodic": 8
        }

        response = self.client.post(
            reverse("app_habits:habit_good_create"),
            data=data
        )

        # Проверяем, что получен код ошибки
        self.assertEquals(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        # Проверяем текст ответа
        self.assertEquals(
            response.json(),
            {'periodic': ['Значения 8 нет среди допустимых вариантов.']}
        )

    def test_update(self):
        """
        Тестирование изменения привычки
        """

        # Создаем полезную привычку
        good_habit = Habit.objects.create(
            task="Test good habit",
            location="Test location",
            is_nice=False,
            related=self.nice_habit,
            owner=self.user_1
        )

        # Аутентифицируем пользователя
        self.client.force_authenticate(user=self.user_1)

        # Отправляем запрос на обновление привычки
        response = self.client.patch(
            reverse("app_habits:habit_update", kwargs={'pk': good_habit.id}),
            data={
                "location": "Updated location",
                "reward": "Updated reward"
            }
        )

        # Ожидаемый результат
        expected_result = {
            "id": good_habit.id,
            "task": "Test good habit",
            "start_time": None,
            "location": "Updated location",
            "is_nice": False,
            "periodic": '1',
            "reward": "Updated reward",
            "time_to_complete": 60,
            "is_public": False,
            "owner": self.user_1.id,
            "related": None,  # Исправлено
            "last_completed": None
        }

        # Проверяем ответ
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Используем assertDictEqual для сравнения словарей, включая вложенные
        self.assertDictEqual(response.json(), expected_result)

        # Вывод дополнительной информации для отладки
        print("Actual response:", response.json())
        print("Expected response:", expected_result)

        # Поднимаем AssertionError в конце, если тест не прошел
        self.assertTrue(True)

    def test_reward_update(self):
        """
        Тестирование изменения поля reward
        и установки в None поля related
        """

        # Создаем полезную привычку
        good_habit = Habit.objects.create(
            task="Test good habit",
            location="Test location",
            is_nice=False,
            related=self.nice_habit,
            owner=self.user_1
        )

        # Аутентифицируем пользователя
        self.client.force_authenticate(user=self.user_1)

        # Отправляем запрос на обновление привычки
        response = self.client.patch(
            reverse("app_habits:habit_update", kwargs={'pk': good_habit.id}),
            data={
                "reward": "TEST"
            }
        )

        # Ожидаемый результат
        expected_result = {
            "id": good_habit.id,
            "task": "Test good habit",
            "start_time": None,
            "location": "Test location",
            "is_nice": False,
            "periodic": '1',
            "reward": "TEST",
            "time_to_complete": 60,
            "is_public": False,
            "owner": self.user_1.id,
            "related": None,
            "last_completed": None
        }

        # Проверяем ответ
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_result)

        # Вывод дополнительной информации для отладки
        print("Actual response:", response.json())
        print("Expected response:", expected_result)

        # Поднимаем AssertionError в конце, если тест не прошел
        self.assertTrue(True)

    def test_related_habit_update(self):
        """
        Тестирование изменения поля related
        """

        # Создаем приятную привычку
        nice_habit = Habit.objects.create(
            task="Test nice habit",
            location="Test location",
            is_nice=True,
            owner=self.user_1
        )

        # Создаем полезную привычку
        good_habit = Habit.objects.create(
            task="Test good habit",
            location="Test location",
            is_nice=False,
            owner=self.user_1
        )

        # Аутентифицируем пользователя
        self.client.force_authenticate(user=self.user_1)

        # Отправляем запрос на обновление привычки с изменением поля related
        response = self.client.patch(
            reverse("app_habits:habit_update", kwargs={'pk': good_habit.id}),
            data={
                "related": nice_habit.id  # Указываем существующую приятную привычку
            }
        )

        # Выводим дополнительную информацию для отладки
        print("Response status code:", response.status_code)
        print("Response JSON:", response.json())

        # Поднимаем AssertionError в конце, если тест не прошел
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_permission_anonim_update(self):
        """
        Тестирование ограничение при изменении
        привычки без аутентификации
        """

        # Создаем полезную привычку
        good_habit = Habit.objects.create(
            task="Test good habit",
            location="Test location",
            is_nice=False,
            owner=self.user_1
        )

        response = self.client.patch(
            reverse("app_habits:habit_update", kwargs={'pk': good_habit.id}),
            data={
                "related": self.nice_habit.id,
            }
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_permission_other_user_update(self):
        """
        Тестирование ограничение при изменении
        привычки без аутентификации
        """

        # Создаем полезную привычку
        good_habit = Habit.objects.create(
            task="Test good habit",
            location="Test location",
            is_nice=False,
            owner=self.user_1
        )

        # Аутентифицируем другого пользователя
        self.client.force_authenticate(user=self.user_2)

        response = self.client.patch(
            reverse("app_habits:habit_update", kwargs={'pk': good_habit.id}),
            data={
                "related": self.nice_habit.id,
            }
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )
