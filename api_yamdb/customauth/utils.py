import random
import string
from django.core.mail import send_mail
from users.models import CustomUser


def generate_and_send_confirmation_code(user: CustomUser):
    confirmation_code = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    user.confirmation_code = confirmation_code
    user.save()

    send_mail(
        subject='Код подтверждения',
        message=f'Ваш код подтверждения: {confirmation_code}',
        from_email='yamdb@yamdb.com',
        recipient_list=[user.email],
    )
    return confirmation_code
