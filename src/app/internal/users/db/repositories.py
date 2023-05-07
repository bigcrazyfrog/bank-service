from typing import Optional, List

from app.internal.users.db.models import User, validate_phone, RefreshToken
from app.internal.users.domain.entities import UserOut, UserIn, NotFoundException
from app.internal.users.domain.services import IUserRepository


class UserRepository(IUserRepository):
    def get_user_by_id(self, id: str) -> UserOut:
        user: Optional[User] = User.objects.filter(id=id).first()
        if user is None:
            raise NotFoundException(name="User", id=id)

        return UserOut.from_orm(user)

    def add_user(self, user_data: UserIn) -> bool:
        user, created = User.objects.get_or_create(id=user_data.id, defaults={"name": user_data.name})
        return created

    def update_fields(self, id: str, fields: dict) -> None:
        user, _ = User.objects.get_or_create(id=id)

        user.__dict__.update(fields)
        user.save()

    def get_favorite_list(self, id: str) -> List[str] | None:
        user: Optional[User] = User.objects.filter(id=id).first()
        if user is None:
            raise NotFoundException(name="User", id=id)

        favorite_list = user.favorite_users.values_list("id", flat=True)
        return list(favorite_list)

    def add_favorite(self, id: str, favorite_user_id: str) -> None:
        user: Optional[User] = User.objects.filter(id=id).first()
        favorite_user: Optional[User] = User.objects.filter(id=favorite_user_id).first()

        if user is None:
            raise NotFoundException(name="User", id=id)
        if favorite_user is None:
            raise NotFoundException(name="User", id=favorite_user_id)

        user.favorite_users.add(favorite_user)
        user.save()

    def remove_favorite(self, id: str, favorite_user_id: str) -> None:
        user: Optional[User] = User.objects.filter(id=id).first()
        favorite_user: Optional[User] = User.objects.filter(id=favorite_user_id).first()

        if user is None:
            raise NotFoundException(name="User", id=id)
        if favorite_user is None:
            raise NotFoundException(name="User", id=favorite_user_id)

        user.favorite_users.remove(favorite_user)
        user.save()

    def is_correct_password(self, user_id: str, password: str) -> bool:
        origin_password = User.objects.filter(id=user_id).values_list('password', flat=True).first()
        return password == origin_password

    def token_exists(self, token: str) -> bool:
        return RefreshToken.objects.filter(jti=token).exists()

    def get_token(self, token: str) -> RefreshToken:
        return RefreshToken.objects.filter(jti=token).first()

    def revoke_token(self, token: str) -> None:
        RefreshToken.objects.filter(jti=token).update(revoked=True)

    def revoke_all_tokens(self, user_id: str) -> None:
        RefreshToken.objects.filter(user__id=user_id).update(revoked=True)
