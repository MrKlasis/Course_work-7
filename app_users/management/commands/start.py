from django.core.management import BaseCommand

from app_habits.services import start


class Command(BaseCommand):

    def handle(self, *args, **options):
        start()
