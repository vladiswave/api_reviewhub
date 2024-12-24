from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import CustomUser


class UserSerializerForAdmins(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=254,
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )
    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=[
            RegexValidator(regex=r'^[\w.@+-]+\Z'),
            UniqueValidator(queryset=CustomUser.objects.all())
        ]
    )
    role = serializers.ChoiceField(
        choices=CustomUser.ROLE_CHOICES,
        default='user'
    )
    first_name = serializers.CharField(
        max_length=150,
        required=False
    )
    last_name = serializers.CharField(
        max_length=150,
        required=False
    )

    def validate(self, data):
        username = data.get('username')

        if username == 'me':
            raise serializers.ValidationError(
                'Username "me" использовать нельзя.'
            )

        return data

    class Meta:
        model = CustomUser
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class UserSerializerForAll(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=254,
        allow_blank=False,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )
    username = serializers.CharField(
        max_length=150,
        allow_blank=False,
        validators=[
            RegexValidator(regex=r'^[\w.@+-]+\Z'),
            UniqueValidator(queryset=CustomUser.objects.all())
        ]
    )
    role = serializers.ChoiceField(
        choices=CustomUser.ROLE_CHOICES,
        read_only=True
    )
    first_name = serializers.CharField(
        max_length=150,
        required=False
    )
    last_name = serializers.CharField(
        max_length=150,
        required=False
    )

    def validate(self, data):
        username = data.get('username')

        if username == 'me':
            raise serializers.ValidationError(
                'Username "me" использовать нельзя.'
            )

        return data

    class Meta:
        model = CustomUser
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
