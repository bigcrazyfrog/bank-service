from django.contrib import admin

from app.internal.users.db.models import User, RefreshToken


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(RefreshToken)
class RefreshTokenAdmin(admin.ModelAdmin):
    pass
