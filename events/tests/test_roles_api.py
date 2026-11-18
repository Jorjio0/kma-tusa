import pytest

from events.models import Category


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
def test_admin_cannot_delete_category_with_events(admin_client, event):
    response = admin_client.delete(f"/api/categories/{event.category.id}/")
    assert response.status_code == 409
    assert "тусовки (1)" in response.data["detail"]
