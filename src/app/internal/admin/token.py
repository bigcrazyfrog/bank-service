from django.contrib import admin

from app.internal.models.token import AccessToken, RefreshToken


@admin.register(AccessToken)
class AccessTokenAdmin(admin.ModelAdmin):
    pass


@admin.register(RefreshToken)
class RefreshTokenAdmin(admin.ModelAdmin):
    pass
