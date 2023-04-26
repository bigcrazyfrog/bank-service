import datetime

import jwt

from app.internal.models.token import RefreshToken
from app.internal.services.user_service import UserService
from config.settings import (
    JWT_ACCESS_SECRET,
    JWT_ACCESS_TOKEN_LIFETIME,
    JWT_REFRESH_SECRET,
    JWT_REFRESH_TOKEN_LIFETIME,
    SALT,
)


class AuthService:
    @staticmethod
    def token_exists(token: str) -> bool:
        return RefreshToken.objects.filter(jti=token).exists()

    @staticmethod
    def is_revoked_token(token: str) -> bool:
        refresh_token = RefreshToken.objects.filter(jti=token).first()
        if refresh_token.revoked:
            return True

        try:
            payload = jwt.decode(token, JWT_ACCESS_SECRET, algorithms=["HS256"])
        except jwt.exceptions.ExpiredSignatureError:
            return None

        date = datetime.datetime.strptime(payload["date"], '%Y-%m-%d %H:%M:%S.%f')
        return date < datetime.datetime.now()

    @staticmethod
    def check_access_token(token: str) -> bool:
        try:
            payload = jwt.decode(token, JWT_ACCESS_SECRET, algorithms=["HS256"])
        except jwt.exceptions.ExpiredSignatureError:
            return False

        date = datetime.datetime.strptime(payload["date"], '%Y-%m-%d %H:%M:%S.%f')
        return date > datetime.datetime.now()

    @staticmethod
    def get_user_id(token: str) -> str | None:
        try:
            payload = jwt.decode(token, JWT_ACCESS_SECRET, algorithms=["HS256"])
        except jwt.exceptions.ExpiredSignatureError:
            return None

        return payload["id"]

    @staticmethod
    def revoke_token(token: str) -> None:
        RefreshToken.objects.filter(jti=token).update(revoked=True)

    @staticmethod
    def revoke_all_tokens(token: str) -> None:
        user_id = AuthService.get_user_id(token)
        RefreshToken.objects.filter(user__id=user_id).update(revoked=True)

    @staticmethod
    def generate_tokens(user_id: str) -> dict:
        access_token = AuthService.generate_access_token(user_id)
        refresh_token = AuthService.generate_refresh_token(user_id)

        user = UserService.get_user(user_id)
        RefreshToken.objects.create(jti=refresh_token, user=user)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

    @staticmethod
    def generate_access_token(user_id):
        date = str(datetime.datetime.now() + JWT_ACCESS_TOKEN_LIFETIME)
        return jwt.encode({"id": user_id, "admin": False, "date": date}, JWT_ACCESS_SECRET, algorithm="HS256")

    @staticmethod
    def generate_refresh_token(user_id: str):
        date = str(datetime.datetime.now() + JWT_REFRESH_TOKEN_LIFETIME)
        return jwt.encode({"id": user_id, "date": date}, JWT_REFRESH_SECRET, algorithm="HS256")
