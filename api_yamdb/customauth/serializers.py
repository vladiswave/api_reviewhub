from rest_framework import serializers
from rest_framework_simplejwt.tokens import AccessToken
from users.models import CustomUser
from customauth.utils import generate_confirmation_code, send_confirmation_email
from rest_framework.exceptions import ValidationError, NotFound
from customauth.validators import validate_username_reserved, validate_username_regex, validate_email_username_conflict


class UserRegistrationSerializer(serializers.Serializer):
    """Сериализатор для регистрации пользователей без аутентификации."""

    email = serializers.EmailField(
        max_length=254,
    )
    username = serializers.CharField(
        max_length=150,
        allow_blank=False,
    )

    def validate(self, attrs):
        email = attrs.get('email')
        username = attrs.get('username')

        validate_username_reserved(username)
        validate_username_regex(username)
        validate_email_username_conflict(email, username)

        return super().validate(attrs)

    def create(self, attrs):
        username = attrs.get('username')

        validate_username_reserved(username)
        validate_username_regex(username)

        confirmation_code = generate_confirmation_code()

        try:
            user = CustomUser.objects.get(username=username)
            user.confirmation_code = confirmation_code
            user.save()
        except CustomUser.DoesNotExist:
            user = CustomUser.objects.create(
                username=username,
                email=attrs.get('email'),
                confirmation_code=confirmation_code
            )
        send_confirmation_email(user.email, confirmation_code)
        return user


class CustomTokenSerializer(serializers.Serializer):
    """Сериализатор для получения токенов."""

    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=8)

    def validate(self, attrs):
        username = attrs['username']
        validate_username_reserved(username)
        validate_username_regex(username)
        confirmation_code = attrs['confirmation_code']

        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            raise NotFound('Проверьте username.')

        if user.confirmation_code != confirmation_code:
            raise ValidationError('Неправильный код.')

        return {'access': str(AccessToken.for_user(user))}
