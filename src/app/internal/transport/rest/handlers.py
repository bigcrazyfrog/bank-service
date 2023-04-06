from asgiref.sync import async_to_sync
from django.http import JsonResponse

from app.internal.services.user_service import User
from app.internal.models.admin_user import UserProfile


def user_info(request, telegram_id):
    return JsonResponse(User.info(telegram_id))
