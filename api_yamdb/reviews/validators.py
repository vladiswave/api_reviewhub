from django.utils import timezone

from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


characters_validator = RegexValidator(
    r'^[-a-zA-Z0-9_]+$',
    'Символы латинского алфавита, цифры и знак подчёркивания'
)


def validate_year(value):
    if not (value < timezone.now().year):
        raise ValidationError('Год выпуска не может быть больше текущего')
