import hashlib
from datetime import datetime
from typing import Optional

import jwt

from app.internal.auth.domain.entities import Tokens
from app.internal.users.domain.entities import UserIn, UserOut
from config.settings import (
    JWT_ACCESS_SECRET,
    JWT_ACCESS_TOKEN_LIFETIME,
    JWT_REFRESH_SECRET,
    JWT_REFRESH_TOKEN_LIFETIME,
    SALT,
)


class IAuthRepository:
    """Interface for authentication repository."""

    def register_user(self, user_data: UserIn) -> bool:
        ...


class AuthService:
    """Authentication service."""

    def __init__(self, auth_repo: IAuthRepository):
        self._auth_repo = auth_repo

    def register_user(self, user_data: UserIn) -> bool:
        """Register new user."""
        user_data.password = self.hash_password(password=user_data.password)
        return self._auth_repo.register_user(user_data=user_data)

    @classmethod
    def hash_password(cls, password: str) -> str:
        """Hash password.

        Hashing by SHA512 hash algorithm with adding salt.

        """
        return hashlib.sha512(password.encode() + SALT.encode()).hexdigest()

    def is_correct_password(self, id: str, password: str) -> bool:
        """Check is correct password."""
        hash_password = AuthService.hash_password(password)
        return self._auth_repo.is_correct_password(id=id, password=hash_password)

    def token_exists(self, token: str) -> bool:
        """Check token existing."""
        return self._auth_repo.token_exists(token=token)

    def is_revoked_token(self, token: str) -> bool:
        """Check if token is revoked."""
        refresh_token = self._auth_repo.get_token(token=token)
        if refresh_token.revoked:
            return True

        try:
            payload = jwt.decode(token, JWT_ACCESS_SECRET, algorithms=["HS256"])
        except jwt.exceptions.ExpiredSignatureError:
            return None

        date = datetime.strptime(payload["date"], '%Y-%m-%d %H:%M:%S.%f')
        return date < datetime.now()

    def check_access_token(self, token: str) -> bool:
        """Valid access token."""
        try:
            payload = jwt.decode(token, JWT_ACCESS_SECRET, algorithms=["HS256"])
        except jwt.exceptions.ExpiredSignatureError:
            return False

        date = datetime.strptime(payload["date"], '%Y-%m-%d %H:%M:%S.%f')
        return date > datetime.now()

    def get_user_id(self, token: str) -> Optional[str]:
        """Get user ID from access token."""
        try:
            payload = jwt.decode(token, JWT_ACCESS_SECRET, algorithms=["HS256"])
        except jwt.exceptions.ExpiredSignatureError:
            return None

        return payload["id"]

    def revoke_token(self, token: str) -> None:
        """Revoke old refresh token."""
        self._auth_repo.revoke_token(token=token)

    def revoke_all_tokens(self, token: str) -> None:
        """Revoke all user's refresh tokens."""
        user_id = self.get_user_id(token=token)
        self._auth_repo.revoke_all_tokens(user_id=user_id)

    def generate_tokens(self, user_id: str) -> Tokens:
        """Generate a pair of tokens for user."""
        access_token = self._generate_access_token(user_id)
        refresh_token = self._generate_refresh_token(user_id)

        self._auth_repo.create_token(refresh_token=refresh_token, user_id=user_id)

        return Tokens(access_token=access_token, refresh_token=refresh_token)

    def _generate_access_token(self, user_id: str) -> str:
        date = str(datetime.now() + JWT_ACCESS_TOKEN_LIFETIME)
        return jwt.encode({"id": str(user_id), "admin": False, "date": date}, JWT_ACCESS_SECRET, algorithm="HS256")

    def _generate_refresh_token(self, user_id: str) -> str:
        date = str(datetime.now() + JWT_REFRESH_TOKEN_LIFETIME)
        return jwt.encode({"id": str(user_id), "date": date}, JWT_REFRESH_SECRET, algorithm="HS256")
