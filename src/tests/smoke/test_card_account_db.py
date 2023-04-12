import pytest

from app.internal.models.account_card import Account, Card
from app.internal.models.admin_user import User


@pytest.mark.smoke
@pytest.mark.django_db
def test_create_account():
    user = User.objects.create(id="1")

    assert Account.objects.count() == 0
    Account.objects.create(number=10**10, owner=user)
    assert Account.objects.count() == 1


@pytest.mark.smoke
@pytest.mark.django_db
def test_get_account():
    user = User.objects.create(id="1")
    account = Account.objects.create(number=10**10, owner=user)

    assert Account.objects.get(number=account.number) == account


@pytest.mark.smoke
@pytest.mark.django_db
def test_get_not_exist_user():
    with pytest.raises(Account.DoesNotExist):
        Account.objects.get(number=10**10)


@pytest.mark.smoke
@pytest.mark.django_db
def test_create_card():
    user = User.objects.create(id="1")
    account = Account.objects.create(number=10**10, owner=user)

    assert Card.objects.count() == 0
    Card.objects.create(number=10**16, account=account)
    assert Card.objects.count() == 1


@pytest.mark.smoke
@pytest.mark.django_db
def test_get_card():
    user = User.objects.create(id="1")
    account = Account.objects.create(number=10**10, owner=user)
    card = Card.objects.create(number=10**16, account=account)

    assert Card.objects.get(number=card.number) == card


@pytest.mark.smoke
@pytest.mark.django_db
def test_get_not_exist_card():
    with pytest.raises(Card.DoesNotExist):
        Card.objects.get(number=10**16)
