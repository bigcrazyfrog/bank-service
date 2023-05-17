from django.core.files.storage import default_storage
from django.http import HttpRequest, JsonResponse
from ninja import NinjaAPI
from ninja.security import HttpBearer

from app.internal.auth.db.exceptions import AlreadyExistException
from app.internal.auth.db.repositories import AuthRepository
from app.internal.auth.domain.services import AuthService
from app.internal.auth.presentation.handlers import AuthHandlers
from app.internal.auth.presentation.routers import add_auth_router
from app.internal.bank.db.repositories import BankRepository
from app.internal.bank.domain.services import BankService
from app.internal.bank.presentation.handlers import BankHandlers
from app.internal.bank.presentation.routers import add_banks_router
from app.internal.storage.domain.service import StorageService
from app.internal.users.db.exceptions import IncorrectPasswordError

from app.internal.users.db.repositories import NotFoundException, UserRepository
from app.internal.users.domain.services import UserService
from app.internal.users.presentation.handlers import UserHandlers
from app.internal.users.presentation.routers import add_users_router


class HTTPJWTAuth(HttpBearer):
    def __init__(self, auth_service: AuthService):
        super().__init__()
        self._auth_service = auth_service

    def authenticate(self, request: HttpRequest, token: str) -> str | None:
        if not self._auth_service.check_access_token(token):
            return None

        user = self._auth_service.get_user_id(token)
        if user is None:
            return None

        request.user = user
        return token


def get_api():
    user_repo = UserRepository()
    user_service = UserService(user_repo=user_repo)
    user_handlers = UserHandlers(user_service=user_service)

    storage_service = StorageService(default_storage)

    bank_repo = BankRepository()
    bank_service = BankService(bank_repo=bank_repo)
    bank_handlers = BankHandlers(bank_service=bank_service, storage_service=storage_service)

    auth_repo = AuthRepository()
    auth_service = AuthService(auth_repo=auth_repo)
    auth_handlers = AuthHandlers(auth_service=auth_service)

    auth = [HTTPJWTAuth(auth_service=auth_service)]

    api = NinjaAPI(
        title='DT.EDU.BACKEND',
        version='1.0.0',
        auth=auth,
    )

    add_auth_router(api, auth_handlers)
    add_users_router(api, user_handlers)
    add_banks_router(api, bank_handlers)

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


@ninja_api.exception_handler(AlreadyExistException)
def already_exist_exception_handler(request, exc):
    return ninja_api.create_response(
        request,
        {"message": f"{exc.name} {exc.id} is already exist"},
        status=400,
    )

@ninja_api.exception_handler(Exception)
def exception_handler(request, exc):
    return ninja_api.create_response(
        request,
        {"message": str(exc)},
        status=400,
    )