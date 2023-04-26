from django.contrib import admin

from app.internal.models.token import RefreshToken


@admin.register(RefreshToken)
class RefreshTokenAdmin(admin.ModelAdmin):
    pass
