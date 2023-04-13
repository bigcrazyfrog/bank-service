import pytest


@pytest.mark.unit
@pytest.mark.django_db
def test_new_user_info(user_service, new_user):
    user = new_user()
    info = user_service.info(user.id)

    assert info['exist'] == True
    assert info['id'] == user.id
    assert info['phone_number'] == user.phone_number


@pytest.mark.unit
@pytest.mark.django_db
def test_no_exist_user_info(user_service):
    info = user_service.info("1")

    assert info['exist'] == False
    assert info['id'] is None
    assert info['phone_number'] is None


@pytest.mark.unit
@pytest.mark.django_db
def test_favorite_add(user_service, new_user):
    first_user = new_user("1")
    second_user = new_user("2")
    third_user = new_user("3")

    success = user_service.add_favorite(first_user.id, second_user.id)
    assert success == True

    favorite_list = user_service.get_favorite_list(first_user.id)
    assert favorite_list == [second_user.id]

    success = user_service.add_favorite(first_user.id, third_user.id)
    assert success == True

    favorite_list = user_service.get_favorite_list(first_user.id)
    assert favorite_list == [second_user.id, third_user.id]


@pytest.mark.unit
@pytest.mark.django_db
def test_favorite_add_incorrect(user_service, new_user):
    first_user = new_user("1")

    success = user_service.add_favorite(first_user.id, "2")
    assert success == False

    favorite_list = user_service.get_favorite_list(first_user.id)
    assert favorite_list == []


@pytest.mark.unit
@pytest.mark.django_db
def test_favorite_add_double(user_service, new_user):
    first_user = new_user("1")
    second_user = new_user("2")

    success = user_service.add_favorite(first_user.id, second_user.id)
    assert success == True
    success = user_service.add_favorite(first_user.id, second_user.id)
    assert success == True

    favorite_list = user_service.get_favorite_list(first_user.id)
    assert favorite_list == [second_user.id]


@pytest.mark.unit
@pytest.mark.django_db
def test_favorite_remove(user_service, new_user):
    first_user = new_user("1")
    second_user = new_user("2")

    success = user_service.add_favorite(first_user.id, second_user.id)
    assert success == True
    success = user_service.remove_favorite(first_user.id, second_user.id)
    assert success == True

    favorite_list = user_service.get_favorite_list(first_user.id)
    assert favorite_list == []
