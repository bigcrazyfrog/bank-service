from django.db import models


class Account(models.Model):
    number = models.PositiveBigIntegerField(
        verbose_name='Account number',
        primary_key=True,
        unique=True,
        null=False,
    )

    user_profile = models.ForeignKey(
        to='UserProfile',
        on_delete=models.SET_NULL,
        verbose_name='User profile',
        null=True,
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

    account = models.ForeignKey(
        to='Account',
        on_delete=models.CASCADE,
        verbose_name='Account number',
        null=False,
    )

    balance = models.BigIntegerField(
        verbose_name='Balance',
        null=False,
        default=0,
    )

    def __str__(self):
        return f"{self.number}"

    class Meta:
        verbose_name = 'Card'
        verbose_name_plural = 'Cards'
