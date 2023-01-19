from celery import shared_task
from django.conf import settings

from helpers.send_to_third_party import third_party_call


@shared_task(
    name=settings.THIRD_PARTY_MANAGER_TASK,
    autoretry_for=(Exception, ),
    max_retries=3
)
def third_party_manager(message: dict, target: str, message_mode: str = 'html', **kwargs):
    third_party_call(message, target, message_mode=message_mode, **kwargs)
