from django.db import models


class Periodic(models.TextChoices):
    """ Период выполнения привычки """

    DAY_1 = 1, '1 День'
    DAY_2 = 2, '2 Дня'
    DAY_3 = 3, '3 Дня'
    DAY_4 = 4, '4 Дня'
    DAY_5 = 5, '5 Дней'
    DAY_6 = 6, '6 Дней'
    DAY_7 = 7, '7 Дней'
