from django.core.management import BaseCommand

from app_users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email='admin@sky.pro',
            first_name='Admin',
            last_name='Skypro',
            is_staff=True,
            is_superuser=True
        )

        user.set_password('5080')
        user.save()
