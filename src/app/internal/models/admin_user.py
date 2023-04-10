from django.contrib.auth.models import AbstractUser
from django.db import models


class AdminUser(AbstractUser):
    pass


class User(models.Model):
    id = models.CharField(
        verbose_name='telegram ID',
        primary_key=True,
        max_length = 255,
    )

    phone_number = models.CharField(
        verbose_name='phone number',
        max_length=12,
        null=True,
        blank=True,
        default=None,
    )

    favorite_users = models.ManyToManyField(
        to='self',
        verbose_name='favorite users list',
        symmetrical=False,
    )

    def __str__(self):
        return f"{self.id}"

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
