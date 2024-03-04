from django.contrib import admin

from app_habits.models import Habit


@admin.register(Habit)
class MassageAdmin(admin.ModelAdmin):
    list_display = ('pk', 'owner', 'task', 'related', 'reward', 'start_time', 'periodic',
                    'time_to_complete', 'is_nice', 'is_public')
