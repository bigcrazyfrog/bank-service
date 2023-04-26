from http import HTTPStatus

from django.http import HttpResponseNotFound, HttpRequest, JsonResponse
from ninja import NinjaAPI

from app.internal.services.auth_service import AuthService
from app.internal.services.user_service import UserService
from app.internal.transport.rest.auth import HTTPJWTAuth

api = NinjaAPI()


@api.get("/me", auth=HTTPJWTAuth())
def me(request: HttpRequest) -> JsonResponse:
    user = request.user
    return JsonResponse(UserService.info(user))


@api.get("/login")
def login(request: HttpRequest, username: str, password: str):
    if not UserService.is_correct_password(username, password):
        return JsonResponse({"detail": "Incorrect password or username"}, status=HTTPStatus.UNAUTHORIZED)

    return JsonResponse(AuthService.generate_tokens(username))


@api.post("/update_tokens")
def update_tokens(request: HttpRequest, token: str):
    if not AuthService.token_exists(token):
        return "Invalid token"

    if AuthService.is_revoked_token(token):
        AuthService.revoke_all_tokens(token)
        return "Invalid token"

    username = AuthService.get_user_id(token)
    AuthService.revoke_token(token)
    return JsonResponse(AuthService.generate_tokens(username))