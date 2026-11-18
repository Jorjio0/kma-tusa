import pytest
from django.contrib.auth.models import User

REGISTER_DATA = {
    "username": "olena",
    "first_name": "Олена",
    "email": "olena@example.com",
    "password": "Mohyla2026pass",
    "password_confirm": "Mohyla2026pass",
}


@pytest.mark.django_db
def test_register_creates_user_with_hashed_password(api_client):
    response = api_client.post("/api/auth/register/", REGISTER_DATA, format="json")
    assert response.status_code == 201
    assert "password" not in response.data
    user = User.objects.get(username="olena")
    assert user.password != "Mohyla2026pass"
    assert user.check_password("Mohyla2026pass")


@pytest.mark.django_db
def test_register_without_required_fields_returns_400(api_client):
    response = api_client.post("/api/auth/register/", {}, format="json")
    assert response.status_code == 400
    assert set(response.data) == {"username", "email", "password", "password_confirm"}


@pytest.mark.django_db
def test_register_with_weak_and_different_passwords_returns_400(api_client):
    data = dict(REGISTER_DATA, password="12345678", password_confirm="12345679")
    response = api_client.post("/api/auth/register/", data, format="json")
    assert response.status_code == 400
    assert response.data["password_confirm"] == ["Паролі не збігаються."]
    assert "password" in response.data


@pytest.mark.django_db
def test_register_with_taken_username_and_email_returns_400(api_client, user):
    data = dict(REGISTER_DATA, username="student", email="student@example.com")
    response = api_client.post("/api/auth/register/", data, format="json")
    assert response.status_code == 400
    assert set(response.data) == {"username", "email"}


@pytest.mark.django_db
def test_login_returns_tokens(api_client, user):
    data = {"username": "student", "password": "Mohyla2026pass"}
    response = api_client.post("/api/auth/login/", data, format="json")
    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_login_with_wrong_password_returns_401(api_client, user):
    data = {"username": "student", "password": "wrong"}
    response = api_client.post("/api/auth/login/", data, format="json")
    assert response.status_code == 401
    assert response.data["detail"] == "Неправильне ім'я користувача або пароль."


@pytest.mark.django_db
def test_refresh_returns_new_access_token(api_client, user):
    data = {"username": "student", "password": "Mohyla2026pass"}
    tokens = api_client.post("/api/auth/login/", data, format="json").data
    response = api_client.post(
        "/api/auth/refresh/", {"refresh": tokens["refresh"]}, format="json"
    )
    assert response.status_code == 200
    assert "access" in response.data


@pytest.mark.django_db
def test_refresh_with_invalid_token_returns_401(api_client):
    response = api_client.post("/api/auth/refresh/", {"refresh": "bad"}, format="json")
    assert response.status_code == 401


@pytest.mark.django_db
def test_me_returns_current_user(user_client):
    response = user_client.get("/api/auth/me/")
    assert response.status_code == 200
    assert response.data["username"] == "student"
    assert response.data["is_staff"] is False


@pytest.mark.django_db
def test_me_without_token_returns_401(api_client):
    response = api_client.get("/api/auth/me/")
    assert response.status_code == 401
