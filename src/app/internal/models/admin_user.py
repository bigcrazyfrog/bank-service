from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

import re

RE_NUMBER = r'(^[+0-9]{1,3})*([0-9]{10,11}$)'


def validate_phone(phone_number: str) -> None:
    rule = re.compile(RE_NUMBER)

    if not rule.search(phone_number):
        raise ValidationError("Incorrect phone number")


class AdminUser(AbstractUser):
    pass


class User(models.Model):
    id = models.CharField(
        verbose_name='telegram ID',
        primary_key=True,
        max_length=255,
    )

    name = models.CharField(
        verbose_name='username',
        max_length=32,
        null=True,
        blank=True,
        default=None,
    )

    phone_number = models.CharField(
        verbose_name='phone number',
        max_length=12,
        null=True,
        blank=True,
        default=None,
        validators=[validate_phone],
    )

    favorite_users = models.ManyToManyField(
        to='self',
        verbose_name='favorite users list',
        symmetrical=False,
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
