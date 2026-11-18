import pytest

from events.models import Event


@pytest.mark.django_db
def test_guest_gets_event_list(api_client, event):
    response = api_client.get("/api/events/")
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["title"] == "Посвята першокурсників"


@pytest.mark.django_db
def test_guest_gets_empty_event_list(api_client):
    response = api_client.get("/api/events/")
    assert response.status_code == 200
    assert response.data == []


@pytest.mark.django_db
def test_guest_gets_event_by_id(api_client, event):
    response = api_client.get(f"/api/events/{event.id}/")
    assert response.status_code == 200
    assert response.data["id"] == event.id


@pytest.mark.django_db
def test_get_missing_event_returns_404(api_client):
    response = api_client.get("/api/events/999/")
    assert response.status_code == 404
    assert response.data["detail"] == "Тусовку не знайдено."


@pytest.mark.django_db
def test_create_event_without_token_returns_401(api_client, event_data):
    response = api_client.post("/api/events/", event_data, format="json")
    assert response.status_code == 401
    assert Event.objects.count() == 0


@pytest.mark.django_db
def test_create_event_with_invalid_token_returns_401(api_client, event_data):
    api_client.credentials(HTTP_AUTHORIZATION="Bearer invalidtoken")
    response = api_client.post("/api/events/", event_data, format="json")
    assert response.status_code == 401


@pytest.mark.django_db
def test_user_creates_event(user_client, event_data):
    response = user_client.post("/api/events/", event_data, format="json")
    assert response.status_code == 201
    assert response.data["title"] == "Благодійна вечірка"
    assert Event.objects.filter(title="Благодійна вечірка").exists()


@pytest.mark.django_db
def test_create_event_with_empty_body_returns_400(user_client):
    response = user_client.post("/api/events/", {}, format="json")
    assert response.status_code == 400
    assert "title" in response.data
    assert "starts_at" in response.data


@pytest.mark.django_db
def test_create_event_breaking_business_rules_returns_400(user_client, event_data):
    event_data["ends_at"] = "2026-12-19T20:00:00+02:00"
    event_data["price"] = 100
    event_data["fundraising_url"] = ""
    event_data["capacity"] = 500
    response = user_client.post("/api/events/", event_data, format="json")
    assert response.status_code == 400
    assert set(response.data) == {"ends_at", "price", "fundraising_url", "capacity"}
    assert Event.objects.count() == 0


@pytest.mark.django_db
def test_ticket_without_price_returns_400(user_client, event_data):
    event_data["entry_type"] = "ticket"
    event_data["min_donation"] = None
    response = user_client.post("/api/events/", event_data, format="json")
    assert response.status_code == 400
    assert response.data["price"] == ["Для платного квитка вкажіть ціну більше 0."]


@pytest.mark.django_db
def test_user_updates_event(user_client, event, event_data):
    response = user_client.put(f"/api/events/{event.id}/", event_data, format="json")
    assert response.status_code == 200
    event.refresh_from_db()
    assert event.title == "Благодійна вечірка"


@pytest.mark.django_db
def test_update_event_without_token_returns_401(api_client, event, event_data):
    response = api_client.put(f"/api/events/{event.id}/", event_data, format="json")
    assert response.status_code == 401
    event.refresh_from_db()
    assert event.title == "Посвята першокурсників"


@pytest.mark.django_db
def test_update_missing_event_returns_404(user_client, event_data):
    response = user_client.put("/api/events/999/", event_data, format="json")
    assert response.status_code == 404


@pytest.mark.django_db
def test_user_deletes_event(user_client, event):
    response = user_client.delete(f"/api/events/{event.id}/")
    assert response.status_code == 204
    assert not Event.objects.filter(id=event.id).exists()


@pytest.mark.django_db
def test_delete_event_without_token_returns_401(api_client, event):
    response = api_client.delete(f"/api/events/{event.id}/")
    assert response.status_code == 401
    assert Event.objects.filter(id=event.id).exists()


@pytest.mark.django_db
def test_delete_missing_event_returns_404(user_client):
    response = user_client.delete("/api/events/999/")
    assert response.status_code == 404


@pytest.mark.django_db
def test_patch_is_not_allowed(user_client, event):
    response = user_client.patch(
        f"/api/events/{event.id}/", {"title": "x"}, format="json"
    )
    assert response.status_code == 405
