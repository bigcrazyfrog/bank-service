from typing import List

from django.http import HttpRequest, JsonResponse
from ninja.params import Body, Path

from app.internal.users.domain.entities import (
    NotFoundException,
    SuccessResponse,
    Tokens,
    UserIn,
    UserOut, IncorrectPasswordError,
)
from app.internal.users.domain.services import UserService


class UserHandlers:
    def __init__(self, user_service: UserService):
        self._user_service = user_service

    def get_user_by_id(self, request) -> UserOut:
        user = self._user_service.get_user_by_id(id=request.user)
        return user

    def update_phone(self, request, phone_number: str) -> SuccessResponse:
        self._user_service.update_phone(id=request.user, phone_number=phone_number)
        return SuccessResponse(success=True)

    def get_favorite_list(self, request) -> List[UserOut]:
        return self._user_service.get_favorite_list(id=request.user)

    def add_favorite(self, request, favorite_user_id: str) -> SuccessResponse:
        self._user_service.add_favorite(id=request.user, favorite_user_id=favorite_user_id)
        return SuccessResponse(success=True)

    def remove_favorite(self, request, favorite_user_id: str) -> SuccessResponse:
        self._user_service.remove_favorite(id=request.user, favorite_user_id=favorite_user_id)
        return SuccessResponse(success=True)
