import pytest

from events.models import Category, Venue


@pytest.mark.django_db
def test_guest_gets_category_list(api_client, category):
    response = api_client.get("/api/categories/")
    assert response.status_code == 200
    assert response.data[0]["name"] == "Вечірка"


@pytest.mark.django_db
def test_guest_cannot_create_category(api_client):
    response = api_client.post("/api/categories/", {"name": "Стендап"}, format="json")
    assert response.status_code == 401


@pytest.mark.django_db
def test_user_cannot_create_category(user_client):
    response = user_client.post("/api/categories/", {"name": "Стендап"}, format="json")
    assert response.status_code == 403
    assert response.data["detail"] == "Цю дію може виконати лише адміністратор."
    assert not Category.objects.filter(name="Стендап").exists()


@pytest.mark.django_db
def test_admin_creates_category(admin_client):
    response = admin_client.post("/api/categories/", {"name": "Стендап"}, format="json")
    assert response.status_code == 201
    assert Category.objects.filter(name="Стендап").exists()


@pytest.mark.django_db
def test_admin_cannot_create_duplicate_category(admin_client, category):
    response = admin_client.post("/api/categories/", {"name": "Вечірка"}, format="json")
    assert response.status_code == 400
    assert response.data["name"] == ["Категорія з такою назвою вже існує."]


@pytest.mark.django_db
def test_admin_cannot_delete_category_with_events(admin_client, event):
    response = admin_client.delete(f"/api/categories/{event.category.id}/")
    assert response.status_code == 409
    assert "тусовки (1)" in response.data["detail"]


@pytest.mark.django_db
def test_admin_deletes_empty_category(admin_client, category):
    response = admin_client.delete(f"/api/categories/{category.id}/")
    assert response.status_code == 204


@pytest.mark.django_db
def test_user_cannot_update_venue(user_client, venue):
    data = {
        "name": "Новий лофт",
        "type": "loft",
        "district": "Поділ",
        "address": "вул. 1",
    }
    response = user_client.put(f"/api/venues/{venue.id}/", data, format="json")
    assert response.status_code == 403
    venue.refresh_from_db()
    assert venue.name == "Лофт «Цех»"


@pytest.mark.django_db
def test_admin_updates_venue(admin_client, venue):
    data = {
        "name": "Новий лофт",
        "type": "loft",
        "district": "Поділ",
        "address": "вул. 1",
    }
    response = admin_client.put(f"/api/venues/{venue.id}/", data, format="json")
    assert response.status_code == 200
    assert Venue.objects.get(id=venue.id).name == "Новий лофт"


@pytest.mark.django_db
def test_user_creates_organizer(user_client):
    response = user_client.post(
        "/api/organizers/", {"name": "Нова команда"}, format="json"
    )
    assert response.status_code == 201
