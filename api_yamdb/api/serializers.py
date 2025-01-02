from reviews.models import Category, Comment, Genre, Review, Title
from rest_framework import serializers
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.relations import SlugRelatedField
from rest_framework_simplejwt.tokens import AccessToken

from .constants import (
    MAX_CONFIRMATION_CODE_LENGTH,
    MAX_EMAIL_LENGTH,
    MAX_NAME_FIELD_LENGTH,
    ROLE_CHOICES,
)
from .notifications import (
    generate_confirmation_code,
    send_confirmation_email
)
from .validators import (
    validate_email_username_conflict,
    validate_unique_email,
    validate_unique_username,
    validate_username_regex,
    validate_username_reserved,
)
from users.models import YamdbUser


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор для произведений для GET."""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description', 'category', 'genre', 'rating'
        )


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для произведений для POST и PATCH."""

    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        many=True,
        queryset=Genre.objects.all(),
        slug_field='slug',
        allow_empty=False
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'category', 'genre')

    def to_representation(self, instance):
        return TitleReadSerializer(instance).data


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для обзоров."""

    author = SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'score', 'pub_date', 'author')
        read_only_fields = ('title',)

    def validate(self, data):
        request = self.context['request']
        if request.method == 'POST':
            author = request.user
            title_id = self.context.get('view').kwargs.get('title_id')
            if Review.objects.filter(
                title_id=title_id, author=author
            ).exists():
                raise ValidationError('Вы уже оставили отзыв!')
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев."""

    author = SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'pub_date', 'author')
        read_only_fields = ('review',)


class UserRegistrationSerializer(serializers.Serializer):
    """Сериализатор для регистрации пользователей без аутентификации."""

    email = serializers.EmailField(
        max_length=MAX_EMAIL_LENGTH,
    )
    username = serializers.CharField(
        max_length=MAX_NAME_FIELD_LENGTH,
        allow_blank=False,
    )

    def validate(self, attrs):
        """Валидация вводных данных."""
        username = attrs.get('username')
        validate_username_reserved(username)
        validate_username_regex(username)
        validate_email_username_conflict(attrs.get('email'), username)
        return super().validate(attrs)

    def create(self, attrs):
        """Создание или обновление кода для пользователя."""
        username = attrs.get('username')
        confirmation_code = generate_confirmation_code()
        try:
            user = YamdbUser.objects.get(username=username)
            user.confirmation_code = confirmation_code
            user.save()
        except YamdbUser.DoesNotExist:
            user = YamdbUser.objects.create(
                username=username,
                email=attrs.get('email'),
                confirmation_code=confirmation_code
            )
        send_confirmation_email(user.email, confirmation_code)
        return user


class CustomTokenSerializer(serializers.Serializer):
    """Сериализатор для получения токенов."""

    username = serializers.CharField(max_length=MAX_NAME_FIELD_LENGTH)
    confirmation_code = serializers.CharField(
        max_length=MAX_CONFIRMATION_CODE_LENGTH
    )

    def validate(self, attrs):
        """Валидация вводных данных."""
        try:
            user = YamdbUser.objects.get(username=attrs['username'])
        except YamdbUser.DoesNotExist:
            raise NotFound('Такой Username не найден.')

        if user.confirmation_code != attrs['confirmation_code']:
            raise ValidationError('Неправильный код.')

        return {'token': str(AccessToken.for_user(user))}


class UserSerializerForAdmins(serializers.ModelSerializer):
    """Сериализатор для запросов админа к данным пользователя."""

    email = serializers.EmailField(
        max_length=MAX_EMAIL_LENGTH,
        required=True,
    )
    username = serializers.CharField(
        max_length=MAX_NAME_FIELD_LENGTH,
        required=True,
    )
    role = serializers.ChoiceField(
        choices=ROLE_CHOICES,
        default='user'
    )
    first_name = serializers.CharField(
        max_length=MAX_NAME_FIELD_LENGTH,
        required=False,
        allow_blank=True,
    )
    last_name = serializers.CharField(
        max_length=MAX_NAME_FIELD_LENGTH,
        required=False,
        allow_blank=True,
    )

    class Meta:
        model = YamdbUser
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    def validate(self, attrs):
        """Валидация вводных данных."""
        new_username = attrs.get('username')
        new_email = attrs.get('email')
        if self.instance is None:
            validate_unique_username(new_username)
            validate_unique_email(new_email)
        else:
            if new_username and new_username != self.instance.username:
                validate_unique_username(new_username)
            if new_email and new_email != self.instance.email:
                validate_unique_email(new_email)
        validate_username_reserved(attrs.get('username'))
        validate_username_regex(attrs.get('username'))
        return super().validate(attrs)


class UserSerializerForAll(UserSerializerForAdmins):
    """Сериализатор для собственных данных /me."""

    role = serializers.CharField(
        read_only=True,
    )
