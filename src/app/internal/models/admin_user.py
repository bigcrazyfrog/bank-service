from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class AdminUser(AbstractUser):
    pass


class UserProfile(models.Model):
    telegram_id = models.PositiveIntegerField(
        verbose_name='telegram ID',
        unique=True,
        null=False,
    )
    phone_number = PhoneNumberField(
        verbose_name='phone number',
        null=True,
        blank=True,
        default=None,
    )

    def __str__(self):
        return f"{self.telegram_id}"

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
