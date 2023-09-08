import re

from django.core.exceptions import ValidationError
from django.db import models

RE_NUMBER = r'(^[+0-9]{1,3})*([0-9]{10,11}$)'


def validate_phone(phone_number: str) -> None:
    """Check phone number custom validation.

    Raises:
        ValidationError: If number is not valid.

    """
    rule = re.compile(RE_NUMBER)

    if not rule.search(phone_number):
        raise ValidationError(f"Incorrect phone number - {phone_number}")


class User(models.Model):
    """Custom telegram user model."""

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

    password = models.CharField(
        max_length=255,
        null=True,
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
        blank=True,
    )

    def __str__(self) -> str:
        return f"{self.name}"

    def __repr__(self) -> str:
        return f"User<{self.id}>"

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
