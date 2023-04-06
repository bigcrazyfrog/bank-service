from django.contrib import admin

from app.internal.models.favorite_user import FavouriteUser


@admin.register(FavouriteUser)
class FavouriteUserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user_id', 'favourite_user_id')
