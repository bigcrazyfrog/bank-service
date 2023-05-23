from typing import Optional

from app.internal.auth.db.exceptions import AlreadyExistException
from app.internal.auth.db.models import RefreshToken
from app.internal.auth.domain.services import IAuthRepository
from app.internal.users.db.models import User
from app.internal.users.domain.entities import UserIn, UserOut


class AuthRepository(IAuthRepository):
    def register_user(self, user_data: UserIn) -> bool:
        if User.objects.filter(id=user_data.id).exists():
            raise AlreadyExistException(name="Username", id=user_data.id)

        User.objects.create(id=user_data.id, name=user_data.name, password=user_data.password)
        return True

    def is_correct_password(self, id: str, password: str) -> bool:
        return User.objects.filter(id=id, password=password).exists()

    def token_exists(self, token: str) -> bool:
        return RefreshToken.objects.filter(jti=token).exists()

    def create_token(self, refresh_token, user_id: str):
        user = User.objects.filter(id=user_id).first()
        RefreshToken.objects.create(jti=refresh_token, user=user)

    def get_token(self, token: str) -> Optional[RefreshToken]:
        return RefreshToken.objects.filter(jti=token).first()

    def revoke_token(self, token: str) -> None:
        RefreshToken.objects.filter(jti=token).update(revoked=True)

    def revoke_all_tokens(self, user_id: str) -> None:
        RefreshToken.objects.filter(user__id=user_id).update(revoked=True)
