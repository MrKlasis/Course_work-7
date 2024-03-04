from celery import shared_task

from app_habits.services import send_message_to_telegram


@shared_task
def send_message_tg(**kwargs):
    send_message_to_telegram(**kwargs)
