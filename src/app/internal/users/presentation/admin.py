from django.contrib import admin

from app.internal.users.db.models import RefreshToken, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(RefreshToken)
class RefreshTokenAdmin(admin.ModelAdmin):
    pass
