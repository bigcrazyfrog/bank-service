import pytest
from django.test import Client


@pytest.mark.smoke
def test_admin():
    response = Client().get("/admin/")
    assert response.status_code == 302


@pytest.mark.smoke
@pytest.mark.django_db
def test_user_info():
    response = Client().get("/api/userinfo/197433339/")
    assert response.status_code == 200
