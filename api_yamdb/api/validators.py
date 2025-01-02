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
        message={
            "username": [
                'Username должен состоять из букв, цифр и символов @.+-_'
            ]
        }
    )
    regex_validator(value)


def validate_email_username_conflict(email, username):
    """
    Валидация username и email на уникальность.
    """
    user_with_email = YamdbUser.objects.filter(email=email).first()
    user_with_username = YamdbUser.objects.filter(username=username).first()

    if user_with_email and user_with_username:
        if user_with_email != user_with_username:
            raise ValidationError({
                "username": ["Этот username уже занят."],
                "email": ["Этот email уже занят."]
            })
    elif user_with_email or user_with_username:
        if user_with_username:
            raise ValidationError({"username": ["Этот username уже занят."]})
        if user_with_email:
            raise ValidationError({"email": ["Этот email уже занят."]})


def validate_unique_username(username):
    """Валидация username на уникальность."""
    if YamdbUser.objects.filter(username=username).exists():
        raise ValidationError('Этот username уже занят.')


def validate_unique_email(email):
    """Валидация email на уникальность."""
    if YamdbUser.objects.filter(email=email).exists():
        raise ValidationError('Этот email уже занят.')
