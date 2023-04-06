from django.db import models


class Transaction(models.Model):
    from_card = models.PositiveBigIntegerField(
        verbose_name='From card number',
        null=False,
    )

    to_card = models.PositiveBigIntegerField(
        verbose_name='To card number',
        null=False,
    )

    amount = models.BigIntegerField(
        verbose_name='Amount',
        null=False,
    )

    date = models.DateTimeField(
        verbose_name='Date',
        auto_now_add=True,
    )

    def __str__(self):
        return f"{self.pk}"

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
