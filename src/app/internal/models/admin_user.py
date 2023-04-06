from django.db import models
from django.contrib.auth.models import AbstractUser


class AdminUser(AbstractUser):
    pass


class UserProfile(models.Model):
    telegram_id = models.PositiveIntegerField(
        verbose_name='telegram ID',
        unique=True,
        null=False,
    )

    phone_number = models.CharField(
        verbose_name='phone number',
        max_length=12,
        null=True,
        blank=True,
        default=None,
    )

    def __str__(self):
        return f"{self.telegram_id}"

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
