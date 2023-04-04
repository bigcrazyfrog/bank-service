from django.db import models


class FavoriteUser(models.Model):
    profile = models.ForeignKey(
        to='UserProfile',
        on_delete=models.CASCADE,
        verbose_name='User profile',
        null=False,
    )

    def __str__(self):
        return f"{self.profile}"

    class Meta:
        verbose_name = 'Favorite user'
        verbose_name_plural = 'Favorite users'
