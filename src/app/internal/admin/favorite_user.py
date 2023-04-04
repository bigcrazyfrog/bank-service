from django.contrib import admin

from app.internal.models.favorite_user import FavoriteUser


@admin.register(FavoriteUser)
class FavoriteUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile')
