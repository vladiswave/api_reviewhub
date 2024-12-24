import random
import string

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, max_length=254)
    bio = models.TextField(blank=True)
    ROLE_CHOICES = [
        ('user', 'User'),
        ('moderator', 'Moderator'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(
        max_length=10, choices=ROLE_CHOICES, default='user'
    )
    confirmation_code = models.CharField(max_length=8, blank=True, null=True)
    password = models.CharField(max_length=128, blank=True, null=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    username = models.CharField(unique=True, max_length=150)

    def generate_confirmation_code(self):
        code = ''.join(
            random.choices(string.ascii_letters + string.digits, k=8)
        )
        self.confirmation_code = code
        self.save()
        return code
