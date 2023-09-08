from django.contrib import admin

from app.internal.admin_users.db.models import AdminUser


@admin.register(AdminUser)
class AdminUserAdmin(admin.ModelAdmin):
    """Register administrator user in admin panel."""
