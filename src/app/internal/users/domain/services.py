from abc import ABC, abstractmethod
from typing import List

from app.internal.auth.domain.services import AuthService
from app.internal.users.domain.entities import UserIn, UserOut, UserSchema


class IUserRepository(ABC):
    """Interface for User repository."""

    @abstractmethod
    def get_user_by_id(self, id: str) -> UserOut:
        ...

    @abstractmethod
    def update_phone(self, id: str, phone_number: str) -> None:
        ...

    @abstractmethod
    def set_password(self, id: str, hashed_password: str) -> None:
        ...

    @abstractmethod
    def get_favorite_list(self, id: str) -> List[UserOut]:
        ...

    @abstractmethod
    def add_favorite(self, id: str, favorite_user_id: str) -> None:
        ...

    @abstractmethod
    def remove_favorite(self, id: str, favorite_user_id: str) -> None:
        ...


class UserService:
    """Service contains user's business logic."""

    def __init__(self, user_repo: IUserRepository):
        self._user_repo = user_repo

    def add_user(self, user: UserSchema) -> bool:
        """Add new user."""
        return self._user_repo.add_user(user=user)

    def get_user_by_id(self, id: str) -> UserOut:
        """Get existed user by unique ID."""
        return self._user_repo.get_user_by_id(id=id)

    def update_phone(self, id: str, phone_number: str) -> None:
        """Update user's phone number."""
        self._user_repo.update_phone(id=id, phone_number=phone_number)

    def get_favorite_list(self, id: str) -> List[UserOut]:
        """Get user's favourite list."""
        return self._user_repo.get_favorite_list(id=id)

    def add_favorite(self, id: str, favorite_user_id: str) -> None:
        """Add user to favourite list."""
        self._user_repo.add_favorite(id=id, favorite_user_id=favorite_user_id)

    def remove_favorite(self, id: str, favorite_user_id: str) -> None:
        """Remove user from favourite list."""
        self._user_repo.remove_favorite(id=id, favorite_user_id=favorite_user_id)

    def set_password(self, user_id: str, password: str) -> None:
        """Set new password to user.

        Raises:
            ValueError: If password has incorrect length.

        """
        if len(password) > 255:
            raise ValueError("Password should be shorter.")
        if len(password) < 4:
            raise ValueError("Password should be more the 4 chars.")

        hashed_password = AuthService.hash_password(password=password)
        self._user_repo.set_password(id=user_id, hashed_password=hashed_password)
