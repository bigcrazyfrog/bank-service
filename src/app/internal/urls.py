from django.urls import path

from .transport.rest.handlers import user_info

urlpatterns = [
    path('userinfo/<int:telegram_id>/', user_info)
]
