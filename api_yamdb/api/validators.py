from django.core.validators import RegexValidator
from rest_framework.exceptions import ValidationError


def validate_username_reserved(value):
    if value == 'me':
        raise ValidationError('Username не может быть равен "me".')


validate_username_regex = RegexValidator(
    r'^[\w.@+-]+\Z',
    'Username должен состоять из букв, цифр и символов @.+-_'
)
