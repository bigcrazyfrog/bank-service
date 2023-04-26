from django.db import models


class AccessToken(models.Model):
    jti = models.CharField(max_length=255, primary_key=True)
    user = models.ForeignKey(to='User', related_name='access_token', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    revoked = models.BooleanField(default=False)


class RefreshToken(models.Model):
    jti = models.CharField(max_length=255, primary_key=True)
    user = models.ForeignKey(to='User', related_name='refresh_token', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    revoked = models.BooleanField(default=False)
