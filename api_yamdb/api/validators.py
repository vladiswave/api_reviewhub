from django.core.validators import RegexValidator
from rest_framework.exceptions import ValidationError

from users.models import YamdbUser


def validate_username_reserved(value):
    """Валидация username на запрещенные слова."""
    if value == 'me':
        raise ValidationError('Username не может быть равен "me".')


def validate_username_regex(value):
    """Валидация username на требования к спец. символам."""
    regex_validator = RegexValidator(
        regex=r'^[\w.@+-]+\Z',
        message='Username должен состоять из букв, цифр и символов @.+-_'
    )
    regex_validator(value)


def validate_email_username_conflict(email, username):
    """
    Валидация username и email на уникальность.
    """
    email_exists = YamdbUser.objects.filter(email=email).exists()
    username_exists = YamdbUser.objects.filter(username=username).exists()

    if email_exists != username_exists:
        raise ValidationError(
            'Email и Username должны либо существовать вместе.'
        )


def validate_unique_username(username):
    """Валидация username на уникальность."""
    if YamdbUser.objects.filter(username=username).exists():
        raise ValidationError('Этот Username уже занят.')


def validate_unique_email(email):
    """Валидация email на уникальность."""
    if YamdbUser.objects.filter(email=email).exists():
        raise ValidationError('Этот email уже занят.')
