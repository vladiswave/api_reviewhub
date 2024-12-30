from rest_framework.exceptions import ValidationError
from django.core.validators import RegexValidator
from users.models import CustomUser


def validate_username_reserved(value):
    """Ensure username is not a reserved word."""
    if value == 'me':
        raise ValidationError('Username не может быть равен "me".')


def validate_username_regex(value):
    """Ensure username matches regex requirements."""
    regex_validator = RegexValidator(
        regex=r'^[\w.@+-]+\Z',
        message='Username должен состоять только из букв, цифр и символов @.+-_'
    )
    regex_validator(value)


def validate_email_username_conflict(email, username):
    """
    Ensure email and username either both exist together or both are new.
    """
    email_exists = CustomUser.objects.filter(email=email).exists()
    username_exists = CustomUser.objects.filter(username=username).exists()

    if email_exists != username_exists:
        raise ValidationError('Email и Username должны либо существовать вместе, либо быть новыми.')


def validate_unique_username(username):
    """Ensure username is unique."""
    if CustomUser.objects.filter(username=username).exists():
        raise ValidationError('Этот Username уже занят.')


def validate_unique_email(email):
    """Ensure email is unique."""
    if CustomUser.objects.filter(email=email).exists():
        raise ValidationError('Этот Email уже занят.')
