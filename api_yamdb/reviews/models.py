from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from users.models import YamdbUser
from .validators import validate_year
from .constants import (
    MAX_LENGTH_PREVIEW,
    MAX_NAME_LENGTH,
    MAX_SLUG_LENGTH,
    MIN_SCORE_VALUE,
    MAX_SCORE_VALUE
)


class CategoryGenreBaseModel(models.Model):
    """Абстрактная модель для категорий и жанров."""

    name = models.CharField(
        max_length=MAX_NAME_LENGTH,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=MAX_SLUG_LENGTH,
        unique=True,
        verbose_name='Слаг'
    )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name[:MAX_LENGTH_PREVIEW]


class CommentReviewBaseModel(models.Model):
    """Абстрактная модель для отзывов и комментариев."""

    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        YamdbUser,
        verbose_name='Автор',
        on_delete=models.CASCADE,
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        abstract = True
        ordering = ('-pub_date',)
        default_related_name = '%(class)s' + 's'

    def __str__(self):
        return f'{self.text[:MAX_LENGTH_PREVIEW]} от {self.author}'


class Category(CategoryGenreBaseModel):
    """Модель категорий."""

    class Meta(CategoryGenreBaseModel.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(CategoryGenreBaseModel):
    """Модель жанров."""

    class Meta(CategoryGenreBaseModel.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Модель произведений."""

    name = models.TextField(
        max_length=MAX_NAME_LENGTH,
        verbose_name='Название'
    )
    year = models.SmallIntegerField(
        validators=(validate_year,),
        verbose_name='Год выпуска'
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        related_name='titles'
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        related_name='titles',
        null=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        ordering = ('-year', 'name')
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:MAX_LENGTH_PREVIEW]


class Review(CommentReviewBaseModel):
    """Модель отзывов."""

    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
    )
    score = models.PositiveSmallIntegerField(
        validators=(
            MinValueValidator(
                MIN_SCORE_VALUE,
                message=f'Оценка должна быть не меньше {MIN_SCORE_VALUE}.'
            ),
            MaxValueValidator(
                MAX_SCORE_VALUE,
                message=f'Оценка должна быть не больше {MAX_SCORE_VALUE}.'
            )
        ),
        verbose_name='Оценка'
    )

    class Meta(CommentReviewBaseModel.Meta):
        constraints = (
            models.UniqueConstraint(
                fields=('title', 'author'),
                name='unique_name_owner'
            ),
        )
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Comment(CommentReviewBaseModel):
    """Модель комментариев."""

    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
    )

    class Meta(CommentReviewBaseModel.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
