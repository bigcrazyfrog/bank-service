from typing import Optional

from app.internal.auth.db.exceptions import AlreadyExistException
from app.internal.auth.db.models import RefreshToken
from app.internal.auth.domain.services import IAuthRepository
from app.internal.users.db.models import User
from app.internal.users.domain.entities import UserIn


class AuthRepository(IAuthRepository):
    """Repository for user authentication."""

    def register_user(self, user_data: UserIn) -> bool:
        """Register new user in system.

        Raises:
            AlreadyExistException: If user is already exist.

        Returns:
            True if user was created, False in others.

        """
        if User.objects.filter(id=user_data.id).exists():
            raise AlreadyExistException(name="Username", id=user_data.id)

        User.objects.create(id=user_data.id, name=user_data.name, password=user_data.password)
        return True

    def is_correct_password(self, id: str, password: str) -> bool:
        """Check if password is correct."""
        return User.objects.filter(id=id, password=password).exists()

    def token_exists(self, token: str) -> bool:
        """Check refresh token existing."""
        return RefreshToken.objects.filter(jti=token).exists()

    def create_token(self, refresh_token: str, user_id: str) -> None:
        """Create new token for user."""
        user = User.objects.filter(id=user_id).first()
        RefreshToken.objects.create(jti=refresh_token, user=user)

    def get_token(self, token: str) -> Optional[RefreshToken]:
        """Get token model instance."""
        return RefreshToken.objects.filter(jti=token).first()

    def revoke_token(self, token: str) -> None:
        """Revoke token."""
        RefreshToken.objects.filter(jti=token).update(revoked=True)

    def revoke_all_tokens(self, user_id: str) -> None:
        """Revoke all user's token."""
        RefreshToken.objects.filter(user__id=user_id).update(revoked=True)
