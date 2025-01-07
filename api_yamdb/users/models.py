from django.contrib.auth.models import AbstractUser
from django.db import models

from api.constants import (
    MAX_CONFIRMATION_CODE_LENGTH,
    MAX_EMAIL_LENGTH,
    MAX_NAME_FIELD_LENGTH,
    MAX_ROLE_LENGTH,
    ROLE_ADMIN,
    ROLE_CHOICES,
    ROLE_MODERATOR,
    ROLE_USER,
)
from api.validators import validate_username_regex, validate_username_reserved


class YamdbUser(AbstractUser):
    """Модель пользователей."""

    email = models.EmailField(unique=True, max_length=MAX_EMAIL_LENGTH,
                              verbose_name='Эл. почта')
    bio = models.TextField(blank=True, verbose_name='Биография')
    role = models.CharField(max_length=MAX_ROLE_LENGTH, choices=ROLE_CHOICES,
                            default=ROLE_USER, verbose_name='Роль')
    confirmation_code = models.CharField(
        max_length=MAX_CONFIRMATION_CODE_LENGTH,
        blank=True, null=True, verbose_name='Код подтверждения'
    )
    first_name = models.CharField(max_length=MAX_NAME_FIELD_LENGTH, blank=True,
                                  null=False, verbose_name='Имя')
    last_name = models.CharField(max_length=MAX_NAME_FIELD_LENGTH, blank=True,
                                 null=False, verbose_name='Фамилия')
    username = models.CharField(unique=True, max_length=MAX_NAME_FIELD_LENGTH,
                                verbose_name='Имя пользователя',
                                validators=(validate_username_reserved,
                                            validate_username_regex))

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_admin(self):
        return self.is_superuser or self.is_staff or self.role == ROLE_ADMIN

    @property
    def is_moderator(self):
        return self.role == ROLE_MODERATOR

    def __str__(self):
        return f'{self.username} ({self.role})'
