from rest_framework import serializers
from django.core.validators import RegexValidator
from users.models import CustomUser


class UsernameValidationMixin:
    """Mixin для валидации поля username."""

    def validate_username(self, value):
        self.validate_reserved_username(value)
        self.validate_regex_username(value)
        return value

    @staticmethod
    def validate_reserved_username(value):
        """Проверка на запрещенные имена."""
        if value == 'me':
            raise serializers.ValidationError('Username не может быть равен "me".')

    @staticmethod
    def validate_regex_username(value):
        """Проверка на соответствие регулярному выражению."""
        regex_validator = RegexValidator(
            regex=r'^[\w.@+-]+\Z',
            message='Username должен состоять только из букв, цифр и символов @.+-_.'
        )
        regex_validator(value)


class EmailUsernameTakenMixin:
    """Mixin для проверки уникальности email и username."""

    def validate_email_username_taken(self, email, username):
        """Проверка, что email не привязан к другому username."""
        if CustomUser.objects.filter(email=email).exclude(username=username).exists():
            raise serializers.ValidationError('Этот Email уже занят.')

        if CustomUser.objects.filter(username=username).exclude(email=email).exists():
            raise serializers.ValidationError('Этот Username уже занят.')
