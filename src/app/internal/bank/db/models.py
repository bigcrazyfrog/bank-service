import re

from django.core.exceptions import ValidationError
from django.db import models

RE_ACCOUNT = r'[1-9][0-9]{9}'
RE_CARD = r'[1-9][0-9]{15}'


def validate_account(number: int) -> None:
    rule = re.compile(RE_ACCOUNT)

    if not rule.search(str(number)):
        raise ValidationError(f"Incorrect account number - {number}")


def validate_card(number: int) -> None:
    rule = re.compile(RE_CARD)

    if not rule.search(str(number)):
        raise ValidationError(f"Incorrect card number - {number}")


class Account(models.Model):
    number = models.PositiveBigIntegerField(
        verbose_name='Account number',
        primary_key=True,
        unique=True,
        null=False,
        validators=[validate_account],
    )

    owner = models.ForeignKey(
        verbose_name='User profile',
        to='User',
        on_delete=models.CASCADE,
        null=True,
    )

    balance = models.DecimalField(
        verbose_name='Balance',
        max_digits=12,
        decimal_places=2,
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
        validators=[validate_card],
    )

    account = models.ForeignKey(
        to='Account',
        on_delete=models.CASCADE,
        verbose_name='Account number',
        null=False,
    )

    def __str__(self):
        return f"{self.number}"

    class Meta:
        verbose_name = 'Card'
        verbose_name_plural = 'Cards'


class Transaction(models.Model):
    from_account = models.ForeignKey(
        verbose_name='From account',
        related_name='from_account',
        to='Account',
        on_delete=models.PROTECT,
        null=True,
    )

    to_account = models.ForeignKey(
        verbose_name='To account',
        related_name='to_account',
        to='Account',
        on_delete=models.PROTECT,
        null=True,
    )

    amount = models.DecimalField(
        verbose_name='Amount',
        max_digits=12,
        decimal_places=2,
        null=False,
    )

    date = models.DateTimeField(
        verbose_name='Date',
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.from_account} - {self.to_account}"

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
