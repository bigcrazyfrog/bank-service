from django.db import models


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
