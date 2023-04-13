import pytest


@pytest.mark.unit
@pytest.mark.django_db
def test_new_account(account_service, new_account, new_user):
    user = new_user("1")
    account = new_account("1" * 10, user, 100)

    assert account_service.exist(account.number)


@pytest.mark.unit
@pytest.mark.django_db
def test_not_exist_account(account_service):
    assert account_service.exist("1" * 10) == False


@pytest.mark.unit
@pytest.mark.django_db
def test_balance(account_service, new_account, new_user):
    user = new_user("1")
    account = new_account("1" * 10, user, 100)

    assert account_service.balance(user.id, account.number) == 100


@pytest.mark.unit
@pytest.mark.django_db
def test_zero_balance(account_service, new_account, new_user):
    user = new_user("1")
    account = new_account("1" * 10, user, 0)

    assert account_service.balance(user.id, account.number) == 0


@pytest.mark.unit
@pytest.mark.django_db
def test_balance_not_found(account_service):
    assert account_service.balance("1", "1" * 10) is None


@pytest.mark.unit
@pytest.mark.django_db
def test_balance_incorrect_number(account_service):
    with pytest.raises(ValueError):
        account_service.balance("1", "incorrect_number")


@pytest.mark.unit
@pytest.mark.django_db
def test_send_money(account_service, new_user, new_account):
    user = new_user("1")
    first_account = new_account("1" * 10, user, 10)
    second_account = new_account("2" * 10, user, 100)

    account_service.send_money(second_account.number, first_account.number, 20)

    assert account_service.balance(user.id, first_account.number) == 30
    assert account_service.balance(user.id, second_account.number) == 80


@pytest.mark.unit
@pytest.mark.django_db
def test_send_money_by_id(account_service, new_user, new_account):
    first_user = new_user("1")
    second_user = new_user("2")

    first_account = new_account("1" * 10, first_user, 10)
    second_account = new_account("2" * 10, second_user, 100)

    account_service.send_money_by_id(second_account.number, first_user.id, 20)

    assert account_service.balance(first_user.id, first_account.number) == 30
    assert account_service.balance(second_user.id, second_account.number) == 80


@pytest.mark.unit
@pytest.mark.django_db
def test_get_account_by_card(card_service, new_card, new_user, new_account):
    user = new_user("1")
    account = new_account(10**10, user, 0)
    card = new_card(10**16, account)

    assert card_service.get_account(card.number) == account
    assert card_service.get_account(card.number, user.id) == account


@pytest.mark.unit
@pytest.mark.django_db
def test_get_not_exist_account_by_card(card_service):
    assert card_service.get_account(10**10) is None


@pytest.mark.unit
@pytest.mark.django_db
def test_get_card_list(card_service, new_card, new_user, new_account):
    user = new_user("1")
    account = new_account(10**10, user, 0)

    card_list = card_service.get_list(user.id)
    assert card_list == []

    first_card = new_card(10**16, account)
    card_list = card_service.get_list(user.id)
    assert card_list == [str(first_card.number)]

    second_card = new_card(10**16 + 1, account)
    card_list = card_service.get_list(user.id)
    assert card_list == [str(first_card.number), str(second_card.number)]
