import pytest

from app.internal.models.admin_user import User


@pytest.mark.smoke
@pytest.mark.django_db
def test_create_user():
    assert User.objects.count() == 0
    User.objects.create(id="1")
    assert User.objects.count() == 1


@pytest.mark.smoke
@pytest.mark.django_db
def test_get_user():
    user = User.objects.create(id="1")
    found_user = User.objects.get(id="1")

    assert user == found_user


@pytest.mark.smoke
@pytest.mark.django_db
def test_get_not_exist_user():
    with pytest.raises(User.DoesNotExist):
        User.objects.get(id="1")
