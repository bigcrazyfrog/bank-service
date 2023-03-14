from asgiref.sync import async_to_sync
from django.http import JsonResponse

from app.internal.services.user_service import info
from app.models import UserProfile


def user_info(request, telegram_id):
    return JsonResponse(async_to_sync(info)(telegram_id))
