import pytest

from app.internal.models.account_card import Account, Card
from app.internal.models.admin_user import User
from app.internal.services.account_card_service import AccountService, CardService
from app.internal.services.user_service import UserService


@pytest.fixture(scope="function")
def user_service():
    return UserService()

@pytest.fixture(scope="function")
def account_service():
    return AccountService()

@pytest.fixture(scope="function")
def card_service():
    return CardService()

@pytest.fixture(scope="function")
def new_user():
    def create(id="1111111111", phone_number="88005553535"):
        return User.objects.create(id=id, phone_number=phone_number)

    return create

@pytest.fixture(scope="function")
def new_account():
    def create(number, owner, balance=100):
        return Account.objects.create(number=number, owner=owner, balance=balance)

    return create

@pytest.fixture(scope="function")
def new_card():
    def create(number, account):
        return Card.objects.create(number=number, account=account)

    return create