import pytest

from app.internal.models.account_card import Account
from app.internal.transport.bot.handlers import card_number_enter, to_bank_account, to_telegram_id, translation_type


@pytest.mark.integration
@pytest.mark.parametrize(("text", "result"), [
    ("🆔 Telegram ID", 4),
    ("📝 Счет в банке", 5),
    ("💳 Номер карты", 3),
    ("something_wrong", 2),
    ("", 2),
])
def test_translation_type(update, context, text, result):
    update.message.text = text
    assert translation_type(update, context) == result


@pytest.mark.integration
@pytest.mark.django_db
@pytest.mark.parametrize(("text", "result"), [
    (str(10 ** 16), 1),
    ("not_card", 0),
    ("2" * 16, 0),
    ("", 0),
])
def test_card_number_enter(update, context, card_service, new_user, new_account, new_card, text, result):
    user = new_user("1")
    account = new_account(1 ** 10, user, 0)
    new_card(10 ** 16, account)

    update.effective_chat.id = user.id
    update.message.text = text
    assert card_number_enter(update, context) == result


@pytest.mark.integration
@pytest.mark.django_db
def test_send_to_bank_account(update, context, card_service, account_service, new_user, new_account):
    first_user = new_user("1")
    second_user = new_user("2")
    first_account = new_account(1 ** 10, first_user, 1000)
    second_account = new_account(2 ** 10, second_user, 100)

    update.message.text = second_account.number
    context.user_data = dict()
    context.user_data["from_account"] = first_account.number
    context.user_data["amount"] = 50

    assert to_bank_account(update, context) == -1

    assert Account.objects.get(number=first_account.number).balance == 950
    assert Account.objects.get(number=second_account.number).balance == 150


@pytest.mark.integration
@pytest.mark.django_db
def test_send_to_not_exist_account(update, context, card_service, account_service, new_user, new_account):
    update.message.text = 2 ** 10
    assert to_bank_account(update, context) == 5


@pytest.mark.integration
@pytest.mark.django_db
def test_send_to_telegram_id(update, context, card_service, account_service, new_user, new_account):
    first_user = new_user("1")
    second_user = new_user("2")
    first_account = new_account(1 ** 10, first_user, 1000)
    second_account = new_account(2 ** 10, second_user, 100)

    update.message.text = second_user.id
    context.user_data = dict()
    context.user_data["from_account"] = first_account.number
    context.user_data["amount"] = 50

    assert to_telegram_id(update, context) == -1

    assert Account.objects.get(number=first_account.number).balance == 950
    assert Account.objects.get(number=second_account.number).balance == 150


@pytest.mark.integration
@pytest.mark.django_db
def test_send_to_wrong_telegram_id(update, context, card_service, account_service, new_user, new_account):
    update.message.text = "2"
    assert to_telegram_id(update, context) == 4
