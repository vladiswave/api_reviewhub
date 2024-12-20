from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils import timezone

MAX_LENGTH_PREVIEW = 20


def validate_year(value):
    if not (0 < value < timezone.now().year):
        raise ValidationError('Год выпуска не может быть больше текущего')


class User(AbstractUser):
    """Кастомная модель пользователя."""
    pass


class Category(models.Model):
    """Модель категорий."""
    name = models.CharField(
        max_length=256,
        verbose_name='Название категории'
    )
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name[:MAX_LENGTH_PREVIEW]


class Genre(models.Model):
    """Модель жанров."""
    name = models.CharField(
        max_length=256,
        verbose_name='Название жанра'
    )
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name[:MAX_LENGTH_PREVIEW]


class Title(models.Model):
    """Модель произведений."""
    name = models.TextField(
        max_length=256,
        verbose_name='Название произведения'
    )
    year = models.PositiveIntegerField(
        validators=(validate_year,),
        verbose_name='Год выпуска'
    )
    description = models.TextField(
        verbose_name='Описание произведения',
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        related_name='titles',
        null=True,
        blank=True
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        related_name='titles',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        ordering = ('-year', 'name')
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:MAX_LENGTH_PREVIEW]


class Review(models.Model):
    """Модель отзывов."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    # score =
    pass


class Comment(models.Model):
    """Модель комментариев."""
    pass
