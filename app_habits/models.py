from datetime import date

from django.db import models

from app_habits.const import Periodic
from app_users.models import NULL
from config import settings


class Habit(models.Model):

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Автор', **NULL,
                              related_name='owner')
    task = models.TextField(verbose_name='Действие')
    start_time = models.TimeField(verbose_name='Время начала', **NULL)
    location = models.CharField(max_length=50, verbose_name='Место', **NULL)
    is_nice = models.BooleanField(default=False, verbose_name='Признак приятной привычки')
    related = models.ForeignKey('self', on_delete=models.SET_NULL, verbose_name='Привязка', **NULL)
    periodic = models.CharField(default=Periodic.DAY_1, max_length=2, choices=Periodic.choices,
                                verbose_name='Периодичность', **NULL)
    reward = models.CharField(max_length=50, verbose_name="Вознаграждение", **NULL)
    time_to_complete = models.PositiveIntegerField(default=60, verbose_name="Время на выполнение")
    is_public = models.BooleanField(default=False, verbose_name="Признак публичности")

    def __str__(self):
        return f'{self.task}'

    class Meta:
        verbose_name = 'привычка'
        verbose_name_plural = 'привычки'
