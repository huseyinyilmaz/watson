from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string

User = get_user_model()


def generate_registration_code():
    """Generate a new username that does not exists."""
    registration_code = get_random_string(100)
    if User.objects.filter(
            registration_code=registration_code).exists():
        return generate_registration_code()
    else:
        return registration_code
