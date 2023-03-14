from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from app.internal.models.admin_user import AdminUser, UserProfile


@admin.register(AdminUser)
class AdminUserAdmin(UserAdmin):
    pass


@admin.register(UserProfile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'telegram_id', 'phone_number')
