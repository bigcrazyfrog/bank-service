from django.http import JsonResponse, HttpRequest
from ninja.params import Path, Body

from app.internal.users.domain.entities import UserOut, UserIn, SuccessResponse, Tokens, FavouriteListSchema, \
    NotFoundException
from app.internal.users.domain.services import UserService


class IncorrectPasswordError(Exception):
    pass


class TokenNotExistError(Exception):
    def __init__(self, obj: str) -> None:
        self.obj = obj


class RevokedTokenError(Exception):
    pass


class UserHandlers:
    def __init__(self, user_service: UserService):
        self._user_service = user_service

    def get_user_by_id(self, request, user_id: str = Path(...)) -> UserOut:
        user = self._user_service.get_user_by_id(id=user_id)
        return user

    def add_user(self, request, user_data: UserIn = Body(...)) -> SuccessResponse:
        return SuccessResponse(success=self._user_service.add_user(user_data=user_data))

    def update_phone(self, request, phone_number: str) -> SuccessResponse:
        self._user_service.update_phone(id=request.user, phone_number=phone_number)
        return SuccessResponse(success=True)

    def get_favorite_list(self, request) -> FavouriteListSchema:
        favorite_list = self._user_service.get_favorite_list(id=request.user),
        return FavouriteListSchema(favorite_user=favorite_list)

    def add_favorite(self, request, favorite_user_id: str) -> SuccessResponse:
        self._user_service.add_favorite(id=request.user, favorite_user_id=favorite_user_id)
        return SuccessResponse(success=True)

    def remove_favorite(self, request, favorite_user_id: str) -> SuccessResponse:
        self._user_service.remove_favorite(id=request.user, favorite_user_id=favorite_user_id)
        return SuccessResponse(success=True)

    def login(self, request: HttpRequest, id: str, password: str) -> Tokens:
        if not self._user_service.is_correct_password(user_id=id, password=password):
            raise IncorrectPasswordError()
            # return st.incorrect_password

        tokens = self._user_service.generate_tokens(id)
        return Tokens(
            access_token=tokens["access_token"],
            refresh_token=tokens["refresh_token"],
        )

    def update_tokens(self, request: HttpRequest, token: str):
        if not self._user_service.token_exists(token):
            return NotFoundException(name="Token", id=token)
            # return st.invalid_token
        #
        if self._user_service.is_revoked_token(token):
            self._user_service.revoke_all_tokens(token)
            return NotFoundException(name="Token", id=token)
            # return st.invalid_token

        username = self._user_service.get_user_id(token)
        self._user_service.revoke_token(token)

        tokens = self._user_service.generate_tokens(username)
        return Tokens(
            access_token=tokens["access_token"],
            refresh_token=tokens["refresh_token"],
        )
