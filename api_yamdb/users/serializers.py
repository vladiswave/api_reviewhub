from rest_framework import serializers
from .models import CustomUser
from django.core.validators import RegexValidator
from rest_framework.validators import UniqueValidator


class UserSerializerForAdmins(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=254, required=True, validators=[UniqueValidator(queryset=CustomUser.objects.all())])
    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=[
            RegexValidator(regex=r'^[\w.@+-]+\Z'),
            UniqueValidator(queryset=CustomUser.objects.all())
        ]
    )
    role = serializers.ChoiceField(choices=CustomUser.ROLE_CHOICES, default='user')
    first_name = serializers.CharField(
        max_length=150,
        required=False
    )
    last_name = serializers.CharField(
        max_length=150,
        required=False
    )

    def validate(self, data):
        current_user_id = self.context['request'].user.id
        username = data.get('username')
        email = data.get('email')

        if username and CustomUser.objects.filter(username=username).exclude(id=current_user_id).exists():
            raise serializers.ValidationError("Этот Username занят другим пользователем.")

        if email and CustomUser.objects.filter(email=email).exclude(id=current_user_id).exists():
            raise serializers.ValidationError("Этот Email занят другим пользователем.")

        if username == 'me':
            raise serializers.ValidationError("Username 'me' использовать нельзя.")

        return data

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')


class UserSerializerForAll(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=254, allow_blank=False, validators=[UniqueValidator(queryset=CustomUser.objects.all())])
    username = serializers.CharField(
        max_length=150,
        allow_blank=False,
        validators=[
            RegexValidator(regex=r'^[\w.@+-]+\Z'),
            UniqueValidator(queryset=CustomUser.objects.all())
        ]
    )
    role = serializers.ChoiceField(choices=CustomUser.ROLE_CHOICES, read_only=True)
    first_name = serializers.CharField(
        max_length=150,
        required=False
    )
    last_name = serializers.CharField(
        max_length=150,
        required=False
    )

    def validate(self, data):
        current_user_id = self.context['request'].user.id
        username = data.get('username')
        email = data.get('email')

        if username and CustomUser.objects.filter(username=username).exclude(id=current_user_id).exists():
            raise serializers.ValidationError("Этот Username занят другим пользователем.")

        if email and CustomUser.objects.filter(email=email).exclude(id=current_user_id).exists():
            raise serializers.ValidationError("Этот Email занят другим пользователем.")

        if username == 'me':
            raise serializers.ValidationError("Username 'me' использовать нельзя.")

        return data

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
