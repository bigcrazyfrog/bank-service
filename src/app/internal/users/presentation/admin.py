from django.contrib import admin

from app.internal.users.db.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Register user model in admin panel."""
