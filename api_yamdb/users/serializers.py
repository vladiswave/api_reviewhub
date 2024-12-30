from rest_framework import serializers

from users.models import CustomUser
from users.constants import ROLE_CHOICES
from customauth.validators import validate_email_username_conflict, validate_unique_email, validate_unique_username, validate_username_regex, validate_username_reserved

class UserSerializerForAdmins(serializers.ModelSerializer):
    """Сериализатор для запросов админа к данным пользователя."""

    email = serializers.EmailField(
        max_length=254,
        required=True,
    )
    username = serializers.CharField(
        max_length=150,
        required=True,
    )
    role = serializers.ChoiceField(
        choices=ROLE_CHOICES,
        default='user'
    )
    first_name = serializers.CharField(
        max_length=150,
        required=False,
        allow_blank=True,
    )
    last_name = serializers.CharField(
        max_length=150,
        required=False,
        allow_blank=True,
    )

    class Meta:
        model = CustomUser
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    def validate(self, attrs):
        if self.instance is None:
            validate_unique_username(attrs.get('username'))
        validate_username_reserved(attrs.get('username'))
        validate_username_regex(attrs.get('username'))
        validate_unique_email(attrs.get('email'))
        return super().validate(attrs)


class UserSerializerForAll(UserSerializerForAdmins):
    """Сериализатор для собственных данных /me."""
    role = serializers.ChoiceField(
        choices=ROLE_CHOICES,
        default='user',
        read_only=True,
    )

    def validate(self, attrs):
        if 'username' in attrs:
            validate_unique_username(attrs['username'])
            validate_username_reserved(attrs['username'])
            validate_username_regex(attrs['username'])
        if 'email' in attrs:
            validate_unique_username(attrs['email'])
        return super().validate(attrs)
