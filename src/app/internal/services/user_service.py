import hashlib
from typing import List

from app.internal.models.admin_user import User, validate_phone
from config.settings import SALT


def log_errors(f):
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            print(f'error {e}')
            raise e

    return inner


class UserService:
    @staticmethod
    def new_user(telegram_id: str, name: str) -> bool:
        user, created = User.objects.get_or_create(id=telegram_id)
        user.name = name
        user.save(update_fields=("name",))

        return created

    @staticmethod
    def get_user(telegram_id: str) -> User | None:
        user = User.objects.filter(id=telegram_id)
        if not user.exists():
            return None

        return user.first()

    @staticmethod
    def update_phone(telegram_id: str, phone_number: str) -> None:
        validate_phone(phone_number)
        user, _ = User.objects.get_or_create(id=telegram_id)

        user.phone_number = phone_number
        user.save(update_fields=("phone_number",))

    @staticmethod
    def info(telegram_id: str) -> dict:
        user_info = dict(
            exist=False,
            id=None,
            phone_number=None,
        )

        try:
            user = User.objects.get(id=telegram_id)

            user_info['exist'] = True
            user_info['id'] = telegram_id
            user_info['phone_number'] = user.phone_number

        except User.DoesNotExist:
            pass

        return user_info

    @staticmethod
    def set_password(user_id: str, password: str) -> None:
        if len(password) > 255 or len(password) < 4:
            raise ValueError

        user, _ = User.objects.get_or_create(id=user_id)

        user.password = UserService.hash_password(password)
        user.save(update_fields=("password",))

    @staticmethod
    def is_correct_password(user_id: str, password: str) -> bool:
        origin_password = User.objects.filter(id=user_id).values_list('password', flat=True).first()
        return UserService.hash_password(password) == origin_password

    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha512(password.encode() + SALT.encode()).hexdigest()

    @staticmethod
    def get_favorite_list(user_id: str) -> List[User]:
        user = User.objects.get(id=user_id)
        return user.favorite_users.values_list("id", flat=True)

    @staticmethod
    def add_favorite(user_id: str, favorite_user_id: str) -> bool:
        try:
            user = User.objects.get(id=user_id)
            favorite_user = User.objects.get(id=favorite_user_id)
        except User.DoesNotExist:
            return False

        user.favorite_users.add(favorite_user)
        user.save()

        return True

    @staticmethod
    def remove_favorite(user_id: str, favorite_user_id: str) -> bool:
        try:
            user = User.objects.get(id=user_id)
            favorite_user = user.favorite_users.get(id=favorite_user_id)
        except User.DoesNotExist:
            return False

        user.favorite_users.remove(favorite_user)
        user.save()

        return True
