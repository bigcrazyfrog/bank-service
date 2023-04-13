from asgiref.sync import async_to_sync
from django.http import JsonResponse

from app.internal.models.admin_user import User
from app.internal.services.user_service import UserService


def user_info(request, telegram_id):
    return JsonResponse(UserService.info(telegram_id))
