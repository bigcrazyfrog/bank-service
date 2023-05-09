from django.http import HttpRequest, JsonResponse
from ninja import NinjaAPI
from ninja.security import HttpBearer

from app.internal.bank.db.repositories import AccountRepository
from app.internal.bank.domain.services import AccountService
from app.internal.bank.presentation.handlers import AccountHandlers
from app.internal.bank.presentation.routers import add_accounts_router
from app.internal.users.db.repositories import NotFoundException, UserRepository
from app.internal.users.domain.services import UserService
from app.internal.users.presentation.handlers import (
    IncorrectPasswordError,
    RevokedTokenError,
    TokenNotExistError,
    UserHandlers,
)
from app.internal.users.presentation.routers import add_users_router


class HTTPJWTAuth(HttpBearer):
    def __init__(self, user_service: UserService):
        super().__init__()
        self._user_service = user_service

    def authenticate(self, request: HttpRequest, token: str) -> str | None:
        if not self._user_service.check_access_token(token):
            return None

        user = self._user_service.get_user_id(token)
        if user is None:
            return None

        request.user = user
        return token


def get_api():
    user_repo = UserRepository()
    user_service = UserService(user_repo=user_repo)
    user_handlers = UserHandlers(user_service=user_service)
    auth = [HTTPJWTAuth(user_service=user_service)]

    api = NinjaAPI(
        title='DT.EDU.BACKEND',
        version='1.0.0',
        auth=auth,
    )

    account_repo = AccountRepository()
    account_service = AccountService(account_repo=account_repo)
    account_handlers = AccountHandlers(account_service=account_service)

    add_users_router(api, user_handlers)
    add_accounts_router(api, account_handlers)

    return api


ninja_api = get_api()


@ninja_api.exception_handler(NotFoundException)
def user_not_found_exception_handler(request, exc):
    return ninja_api.create_response(
        request,
        {"message": f"{exc.name} with id {exc.id} not found"},
        status=400,
    )


@ninja_api.exception_handler(IncorrectPasswordError)
def incorrect_password_exception_handler(request, exc):
    return ninja_api.create_response(
        request,
        {"message": "Incorrect password or username"},
        status=400,
    )
