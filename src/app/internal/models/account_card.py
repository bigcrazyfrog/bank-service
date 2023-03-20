from django.contrib.auth.models import AbstractUser
from django.db import models


class Account(models.Model):
    number = models.PositiveBigIntegerField(
        verbose_name='Account number',
        primary_key=True,
        unique=True,
        null=False,
    )

    telegram_id = models.PositiveIntegerField(
        verbose_name='telegram ID',
        null=False,
    )

    balance = models.IntegerField(
        verbose_name='Balance',
        null=False,
        default=0,
    )

    def __str__(self):
        return f"{self.number}"

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'


class Card(models.Model):
    number = models.PositiveBigIntegerField(
        verbose_name='Card number',
        primary_key=True,
        unique=True,
        null=False,
    )

    account_number = models.ForeignKey(
        to='Account',
        null=False,
        on_delete=models.CASCADE,
    )

    balance = models.IntegerField(
        verbose_name='Balance',
        null=False,
        default=0,
    )

    def __str__(self):
        return f"{self.number}"

    class Meta:
        verbose_name = 'Card'
        verbose_name_plural = 'Cards'
