from typing import List, Optional

from app.internal.users.db.exceptions import NotFoundException
from app.internal.users.db.models import User
from app.internal.users.domain.entities import UserIn, UserOut
from app.internal.users.domain.services import IUserRepository


class UserRepository(IUserRepository):
    """Repository for user model."""

    def get_model_user(self, id: str) -> User:
        """Get user model instance.

        Raises:
            NotFoundException: If user is not found.

        """
        user: Optional[User] = User.objects.filter(id=id).first()
        if user is None:
            raise NotFoundException(name="User", id=id)
        return user

    def add_user(self, user: UserIn) -> bool:
        """Add new user by user schema.

        Return True if user was created, False in other.

        """
        user, created = User.objects.get_or_create(id=user.id)
        return created

    def get_user_by_id(self, id: str) -> UserOut:
        """Get user with user form."""
        user = self.get_model_user(id=id)
        return UserOut.from_orm(user)

    def update_phone(self, id: str, phone_number: str) -> None:
        """Update phone number."""
        user = self.get_model_user(id=id)
        user.phone_number = phone_number
        user.save(update_fields=("phone_number",))

    def set_password(self, id: str, hashed_password: str) -> None:
        """Set new password.

        Args:
            id: User id.
            hashed_password: New hashed password.

        """
        user = self.get_model_user(id=id)
        user.password = hashed_password
        user.save(update_fields=("password",))

    def get_favorite_list(self, id: str) -> List[UserOut]:
        """Get favourite list."""
        user = self.get_model_user(id=id)

        return user.favorite_users.all().values("id", "name", "phone_number")

    def add_favorite(self, id: str, favorite_user_id: str) -> None:
        """Add user to favourite list.

        Args:
            id: ID of list owner.
            favorite_user_id: User id needed to add to list.

        """
        user = self.get_model_user(id=id)
        favorite_user = self.get_model_user(id=favorite_user_id)

        user.favorite_users.add(favorite_user)
        user.save()

    def remove_favorite(self, id: str, favorite_user_id: str) -> None:
        """Remove user to favourite list.

        Args:
            id: ID of list owner.
            favorite_user_id: User id needed remove from list.

        """
        user = self.get_model_user(id=id)
        favorite_user = self.get_model_user(id=favorite_user_id)

        user.favorite_users.remove(favorite_user)
        user.save()
