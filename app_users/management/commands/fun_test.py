from datetime import time, datetime

from django.core.management import BaseCommand

from app_habits.models import Habit
from app_habits.services import checking_readiness
from app_users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        now_h = datetime.now().hour
        now_m = datetime.now().minute
        good_habit = Habit.objects.create(
            task="Test good habit",
            location="Test location",
            is_nice=False,
            start_time=datetime.strptime(f'{now_h}:{now_m}', '%H:%M').time(),
            owner=User.objects.get(pk=5)
        )
        print(checking_readiness())
