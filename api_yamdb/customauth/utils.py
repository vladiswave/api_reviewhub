import random
import string
from django.core.mail import send_mail
from django.conf import settings


def generate_confirmation_code():
    """Функция генерации кода подтверждения."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))


def send_confirmation_email(user_email, confirmation_code):
    """Функция отправки кода подтверждения."""

    send_mail(
        subject='Confirmation Code',
        message=f'Your confirmation code is: {confirmation_code}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user_email],
    )
