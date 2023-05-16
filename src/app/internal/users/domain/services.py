from typing import List

from app.internal.users.domain.entities import UserIn, UserOut, UserSchema


class IUserRepository:
    def get_user_by_id(self, id: str) -> UserOut:
        ...

    def update_phone(self, id: str, phone_number: str) -> None:
        ...

    def set_password(self, id: str, password: str) -> None:
        ...

    def get_favorite_list(self, id: str) -> List[UserOut]:
        ...

    def add_favorite(self, id: str, favorite_user_id: str) -> None:
        ...

    def remove_favorite(self, id: str, favorite_user_id: str) -> None:
        ...


class UserService:
    def __init__(self, user_repo: IUserRepository):
        self._user_repo = user_repo

    def add_user(self, user: UserSchema):
        return self._user_repo.add_user(user=user)

    def get_user_by_id(self, id: str) -> UserOut:
        return self._user_repo.get_user_by_id(id=id)

    def update_phone(self, id: str, phone_number: str) -> None:
        self._user_repo.update_phone(id=id, phone_number=phone_number)

    def get_favorite_list(self, id: str) -> List[UserOut]:
        return self._user_repo.get_favorite_list(id=id)

    def add_favorite(self, id: str, favorite_user_id: str) -> None:
        self._user_repo.add_favorite(id=id, favorite_user_id=favorite_user_id)

    def remove_favorite(self, id: str, favorite_user_id: str) -> None:
        self._user_repo.remove_favorite(id=id, favorite_user_id=favorite_user_id)

    def set_password(self, user_id: str, password: str) -> None:
        if len(password) > 255 or len(password) < 4:
            raise ValueError

        hash_password = self.hash_password(password),
        self._user_repo.set_password(id=user_id, password=hash_password)
