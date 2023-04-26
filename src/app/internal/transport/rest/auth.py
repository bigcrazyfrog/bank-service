from django.http import HttpRequest
from ninja.security import HttpBearer

from app.internal.services.auth_service import AuthService


class HTTPJWTAuth(HttpBearer):
    def authenticate(self, request: HttpRequest, token: str) -> str | None:
        if not AuthService.check_access_token(token):
            return None

        user = AuthService.get_user_id(token)
        if user is None:
            return None

        request.user = user
        return token
