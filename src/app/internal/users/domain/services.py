import hashlib
import datetime
from typing import List

import jwt

from app.internal.users.db.models import RefreshToken, User
from app.internal.users.domain.entities import UserOut, UserIn
from config.settings import SALT, JWT_ACCESS_SECRET, JWT_ACCESS_TOKEN_LIFETIME, JWT_REFRESH_TOKEN_LIFETIME, \
    JWT_REFRESH_SECRET


class IUserRepository:
    def get_user_by_id(self, id: str) -> UserOut:
        ...

    def add_user(self, user_data: UserIn) -> UserOut:
        ...


class UserService:
    def __init__(self, user_repo: IUserRepository):
        self._user_repo = user_repo

    def get_user_by_id(self, id: str) -> UserOut:
        return self._user_repo.get_user_by_id(id=id)

    def add_user(self, user_data: UserIn) -> bool:
        return self._user_repo.add_user(user_data)

    def update_phone(self, id: str, phone_number: str) -> None:
        fields = {
            "phone_number": phone_number,
        }
        self._user_repo.update_fields(id=id, fields=fields)

    def get_favorite_list(self, id: str) -> List[str] | None:
        return self._user_repo.get_favorite_list(id=id)

    def add_favorite(self, id: str, favorite_user_id: str) -> None:
        self._user_repo.add_favorite(id=id, favorite_user_id=favorite_user_id)

    def remove_favorite(self, id: str, favorite_user_id: str) -> None:
        self._user_repo.remove_favorite(id=id, favorite_user_id=favorite_user_id)

    def set_password(self, user_id: str, password: str) -> None:
        if len(password) > 255 or len(password) < 4:
            raise ValueError

        fields = {
            "password": self.hash_password(password),
        }
        self._user_repo.update_fields(id=user_id, fields=fields)

    def hash_password(self, password: str) -> str:
        return hashlib.sha512(password.encode() + SALT.encode()).hexdigest()

    def is_correct_password(self, user_id: str, password: str) -> bool:
        hash_password = self.hash_password(password)
        return self._user_repo.is_correct_password(user_id=user_id, password=hash_password)

    def token_exists(self, token: str) -> bool:
        return self._user_repo.token_exists(token=token)

    def is_revoked_token(self, token: str) -> bool:
        refresh_token = self._user_repo.get_token(token=token)
        if refresh_token.revoked:
            return True

        try:
            payload = jwt.decode(token, JWT_ACCESS_SECRET, algorithms=["HS256"])
        except jwt.exceptions.ExpiredSignatureError:
            return None

        date = datetime.datetime.strptime(payload["date"], '%Y-%m-%d %H:%M:%S.%f')
        return date < datetime.datetime.now()

    def check_access_token(self, token: str) -> bool:
        try:
            payload = jwt.decode(token, JWT_ACCESS_SECRET, algorithms=["HS256"])
        except jwt.exceptions.ExpiredSignatureError:
            return False

        date = datetime.datetime.strptime(payload["date"], '%Y-%m-%d %H:%M:%S.%f')
        return date > datetime.datetime.now()

    def get_user_id(self, token: str) -> str | None:
        try:
            payload = jwt.decode(token, JWT_ACCESS_SECRET, algorithms=["HS256"])
        except jwt.exceptions.ExpiredSignatureError:
            return None

        return payload["id"]

    def revoke_token(self, token: str) -> None:
        self._user_repo.revoke_token(token=token)

    def revoke_all_tokens(self, token: str) -> None:
        user_id = self.get_user_id(token=token)
        self._user_repo.revoke_all_tokens(user_id=user_id)

    def generate_tokens(self, user_id: str) -> dict:
        access_token = self._generate_access_token(user_id)
        refresh_token = self._generate_refresh_token(user_id)

        user = User.objects.filter(id=user_id).first()
        RefreshToken.objects.create(jti=refresh_token, user=user)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

    def _generate_access_token(self, user_id):
        date = str(datetime.datetime.now() + JWT_ACCESS_TOKEN_LIFETIME)
        return jwt.encode({"id": user_id, "admin": False, "date": date}, JWT_ACCESS_SECRET, algorithm="HS256")

    def _generate_refresh_token(self, user_id: str):
        date = str(datetime.datetime.now() + JWT_REFRESH_TOKEN_LIFETIME)
        return jwt.encode({"id": user_id, "date": date}, JWT_REFRESH_SECRET, algorithm="HS256")
