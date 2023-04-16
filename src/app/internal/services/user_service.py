import re
from typing import List

from app.internal.models.admin_user import User

RE_NUMBER = r'(^[+0-9]{1,3})*([0-9]{10,11}$)'


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
    def new_user(telegram_id: str) -> None:
        User.objects.get_or_create(id=telegram_id)

    @staticmethod
    def update_phone(telegram_id: str, phone: str) -> None:
        rule = re.compile(RE_NUMBER)

        if not rule.search(phone):
            raise ValueError

        user, _ = User.objects.get_or_create(id=telegram_id)

        user.phone_number = phone
        user.save(update_fields=["phone_number"])

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
    def get_favorite_list(user_id: str) -> List[User]:
        user = User.objects.get(id=user_id)

        favorite_list = []
        for favorite_user in user.favorite_users.all():
            favorite_list.append(favorite_user.id)

        return favorite_list

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
