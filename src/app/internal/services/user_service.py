import re

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
    def new_user(telegram_id):
        User.objects.get_or_create(id=telegram_id)

    @staticmethod
    def update_phone(telegram_id, phone):
        rule = re.compile(RE_NUMBER)

        if not rule.search(phone):
            raise ValueError

        user, _ = User.objects.get_or_create(id=telegram_id)

        user.phone_number = phone
        user.save(update_fields=["phone_number"])

    @staticmethod
    def info(telegram_id):
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
