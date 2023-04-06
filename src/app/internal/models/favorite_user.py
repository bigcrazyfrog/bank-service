from django.db import models


class FavouriteUser(models.Model):
    user_id = models.PositiveIntegerField(
        verbose_name='user ID',
        unique=True,
        null=False,
    )

    favourite_user_id = models.PositiveIntegerField(
        verbose_name='favourite user telegram ID',
        unique=True,
        null=False,
    )

    def __str__(self):
        return f"{self.user_id}"

    class Meta:
        verbose_name = 'Favourite user'
        verbose_name_plural = 'Favourite users'
