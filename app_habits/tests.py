from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from app_habits.models import Habit
from app_users.models import User


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
            owner=self.user_1
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
        self.assertEquals(
            response.json(),
            {
                "id": response.json().get("id"),
                "task": "Test task good",
                "start_time": "12:10:00",
                "location": "Test location",
                "is_nice": False,
                "periodic": '1',
                "reward": None,
                "time_to_complete": 60,
                "is_public": False,
                "owner": self.user_1.id,
                "related": None
            }
        )

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

        # Аутентифицируем обычного пользователя
        self.client.force_authenticate(user=self.user_1)

        # Создаем полезную привычку
        Habit.objects.create(
            task="Test good habit",
            location="Test location",
            is_nice=False,
            owner=self.user_1
        )

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

        # Проверяем что получили ошибку
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
        """ Тестирование изменения """

        # Аутентифицируем обычного пользователя
        self.client.force_authenticate(user=self.user_1)

        # Создаем полезную привычку
        good_habit = Habit.objects.create(
            task="Test good habit",
            location="Test location",
            is_nice=False,
            owner=self.user_1
        )

        # Изменяем привычку
        response = self.client.patch(
            reverse("app_habits:habit_update", kwargs={'pk': good_habit.id}),
            data={
                "related": self.nice_habit.id,
            }
        )

        self.assertEquals(
            response.json(),
            {
                'id': good_habit.id,
                'task': 'Test good habit',
                'start_time': None,
                'location': 'Test location',
                'is_nice': False,
                'periodic': '1',
                'reward': None,
                'time_to_complete': 60,
                'is_public': False,
                'owner': self.user_1.id,
                'related': self.nice_habit.id
            }
        )

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

        # Аутентифицируем другого пользователя
        self.client.force_authenticate(user=self.user_1)

        response = self.client.patch(
            reverse("app_habits:habit_update", kwargs={'pk': good_habit.id}),
            data={
                "reward": "TEST"
            }
        )

        self.assertEquals(
            response.json(),
            {
                'id': good_habit.id,
                'task': 'Test good habit',
                'start_time': None,
                'location': 'Test location',
                'is_nice': False,
                'periodic': '1',
                'reward': 'TEST',
                'time_to_complete': 60,
                'is_public': False,
                'owner': self.user_1.id,
                'related': None
            }
        )

    def test_related_habit_update(self):
        """
        Тестирование изменения поля related
        и установки в None поля reward
        """

        # Создаем полезную привычку
        good_habit = Habit.objects.create(
            task="Test good habit",
            location="Test location",
            is_nice=False,
            reward="Test reward",
            owner=self.user_1
        )

        # Аутентифицируем другого пользователя
        self.client.force_authenticate(user=self.user_1)

        response = self.client.patch(
            reverse("app_habits:habit_update", kwargs={'pk': good_habit.id}),
            data={
                "related": self.nice_habit.id,
            }
        )

        self.assertEquals(
            response.json(),
            {
                'id': good_habit.id,
                'task': 'Test good habit',
                'start_time': None,
                'location': 'Test location',
                'is_nice': False,
                'periodic': '1',
                'reward': None,
                'time_to_complete': 60,
                'is_public': False,
                'owner': self.user_1.id,
                'related': self.nice_habit.id
            }
        )

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
