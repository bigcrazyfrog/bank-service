from django.contrib.auth.models import AbstractUser


class AdminUser(AbstractUser):
    """Admin user custom model."""
