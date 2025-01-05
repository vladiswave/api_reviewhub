import random
import string

from django.conf import settings
from django.core.mail import send_mail

from .constants import MAX_CONFIRMATION_CODE_LENGTH


def generate_confirmation_code():
    """Функция генерации кода подтверждения."""
    return ''.join(random.choices(string.ascii_letters + string.digits,
                                  k=MAX_CONFIRMATION_CODE_LENGTH))


def send_confirmation_email(user_email, confirmation_code):
    """Функция отправки кода подтверждения."""
    send_mail(
        subject='Confirmation Code',
        message=f'user_email: {user_email}\n'
                f'confirmation_code: {confirmation_code}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user_email],
    )
