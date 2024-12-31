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
)


class YamdbUser(AbstractUser):
    """Модель пользователей."""

    email = models.EmailField(unique=True, max_length=MAX_EMAIL_LENGTH,
                              verbose_name='Email')
    bio = models.TextField(blank=True, verbose_name='Bio')
    role = models.CharField(max_length=MAX_ROLE_LENGTH, choices=ROLE_CHOICES,
                            default='user', verbose_name='Role')
    confirmation_code = models.CharField(
        max_length=MAX_CONFIRMATION_CODE_LENGTH,
        blank=True, null=True, verbose_name='Confirmation Code'
    )
    first_name = models.CharField(max_length=MAX_NAME_FIELD_LENGTH, blank=True,
                                  null=True, verbose_name='First Name')
    last_name = models.CharField(max_length=MAX_NAME_FIELD_LENGTH, blank=True,
                                 null=True, verbose_name='Last Name')
    username = models.CharField(unique=True, max_length=MAX_NAME_FIELD_LENGTH,
                                verbose_name='Username')
    password = models.CharField(max_length=128, blank=True, null=True)

    @property
    def is_admin(self):
        return self.is_superuser or self.is_staff or self.role == ROLE_ADMIN

    @property
    def is_moderator(self):
        return self.role == ROLE_MODERATOR

    class Meta:
        ordering = ('username',)
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f'{self.username} ({self.role})'
