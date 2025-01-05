MAX_EMAIL_LENGTH = 254
MAX_NAME_FIELD_LENGTH = 150
MAX_PASSWORD_LENGTH = 128
MAX_CONFIRMATION_CODE_LENGTH = 8

ROLE_USER = 'user'
ROLE_MODERATOR = 'moderator'
ROLE_ADMIN = 'admin'

ROLE_CHOICES = (
    (ROLE_USER, 'Пользователь'),
    (ROLE_MODERATOR, 'Модератор'),
    (ROLE_ADMIN, 'Администратор'),
)

MAX_ROLE_LENGTH = max(len(role_name) for role_name, _ in ROLE_CHOICES)
