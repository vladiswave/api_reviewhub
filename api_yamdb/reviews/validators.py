from django.utils import timezone
from django.core.exceptions import ValidationError


def validate_year(value):
    if not (value < timezone.now().year):
        raise ValidationError('Год выпуска не может быть больше текущего')
