import pytest

from app.internal.models.admin_user import User
from app.internal.transport.bot.handlers import add_favorite, remove_favorite, set_phone, start


@pytest.mark.integration
@pytest.mark.django_db
def test_start(update, context, new_user, user_service):
    assert User.objects.count() == 0
    start(update, context)
    assert User.objects.count() == 1


@pytest.mark.integration
@pytest.mark.django_db
def test_set_phone(update, context, new_user, user_service):
    context.args = ["89001110011"]
    set_phone(update, context)

    user = User.objects.get(id=update.effective_chat.id)

    assert user.id == update.effective_chat.id
    assert user.phone_number == context.args[0]


@pytest.mark.integration
@pytest.mark.django_db
def test_set_incorrect_phone(update, context, new_user, user_service):
    User.objects.create(id=update.effective_chat.id, phone_number="89001110011")
    context.args = ["not_phone"]
    set_phone(update, context)

    user = User.objects.get(id=update.effective_chat.id)

    assert user.id == update.effective_chat.id
    assert user.phone_number == "89001110011"


@pytest.mark.integration
@pytest.mark.django_db
def test_add_favorite(update, context, new_user, user_service):
    first_user = new_user("1")
    second_user = new_user("2")

    update.effective_chat.id = first_user.id
    context.args = [second_user.id]

    add_favorite(update, context)

    user = User.objects.get(id=update.effective_chat.id)

    assert user.id == update.effective_chat.id
    assert second_user in user.favorite_users.all()


@pytest.mark.integration
@pytest.mark.django_db
def test_remove_favorite(update, context, new_user, user_service):
    first_user = new_user("1")
    second_user = new_user("2")

    update.effective_chat.id = first_user.id
    context.args = [second_user.id]

    add_favorite(update, context)
    remove_favorite(update, context)

    user = User.objects.get(id=update.effective_chat.id)

    assert user.id == update.effective_chat.id
    assert second_user not in user.favorite_users.all()
