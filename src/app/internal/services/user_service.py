import re

from app.internal.models.admin_user import UserProfile

RE_NUMBER = r'(^[+0-9]{1,3})*([0-9]{10,11}$)'


def log_errors(f):
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            print(f'error {e}')
            raise e

    return inner


class User:
    @staticmethod
    def new_user(telegram_id):
        UserProfile.objects.get_or_create(telegram_id=telegram_id)

    @staticmethod
    def update_phone(telegram_id, phone):
        rule = re.compile(RE_NUMBER)

        if not rule.search(phone):
            raise ValueError

        user, _ = UserProfile.objects.get_or_create(telegram_id=telegram_id)

        user.phone_number = phone
        user.save(update_fields=["phone_number"])

    @staticmethod
    def info(telegram_id):
        user_info = dict(
            exist=False,
            telegram_id=None,
            phone_number=None,
        )

        try:
            user = UserProfile.objects.get(telegram_id=telegram_id)

            user_info['exist'] = True
            user_info['telegram_id'] = telegram_id
            user_info['phone_number'] = user.phone_number

        except UserProfile.DoesNotExist:
            pass

        return user_info
