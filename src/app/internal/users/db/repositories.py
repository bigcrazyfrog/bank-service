from typing import List, Optional

from app.internal.users.db.models import User, validate_phone
from app.internal.users.domain.entities import NotFoundException, UserIn, UserOut
from app.internal.users.domain.services import IUserRepository


class UserRepository(IUserRepository):
    def get_model_user(self, id: str) -> User:
        user: Optional[User] = User.objects.filter(id=id).first()
        if user is None:
            raise NotFoundException(name="User", id=id)

        return user

    def get_user_by_id(self, id: str) -> UserOut:
        user = self.get_model_user(id=id)
        return UserOut.from_orm(user)

    def update_phone(self, id: str, phone_number: str) -> None:
        user = self.get_model_user(id=id)
        user.phone_number = phone_number
        user.save(update_fields=("phone_number",))

    def set_password(self, id: str, password: str) -> None:
        user = self.get_model_user(id=id)
        user.password = password
        user.save(update_fields=("password",))

    def get_favorite_list(self, id: str) -> List[UserOut]:
        user = self.get_model_user(id=id)

        return user.favorite_users.all().values("id", "name", "phone_number")

    def add_favorite(self, id: str, favorite_user_id: str) -> None:
        user = self.get_model_user(id=id)
        favorite_user = self.get_model_user(id=favorite_user_id)

        user.favorite_users.add(favorite_user)
        user.save()

    def remove_favorite(self, id: str, favorite_user_id: str) -> None:
        user = self.get_model_user(id=id)
        favorite_user = self.get_model_user(id=favorite_user_id)

        user.favorite_users.remove(favorite_user)
        user.save()
