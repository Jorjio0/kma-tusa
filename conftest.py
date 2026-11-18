import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from events.models import Category, Event, Organizer, Venue

PASSWORD = "Mohyla2026pass"


def login(client, username):
    response = client.post(
        "/api/auth/login/",
        {"username": username, "password": PASSWORD},
        format="json",
    )
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
    return client


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user(
        username="student", email="student@example.com", password=PASSWORD
    )


@pytest.fixture
def admin_user():
    return User.objects.create_user(
        username="admin", email="admin@example.com", password=PASSWORD, is_staff=True
    )


@pytest.fixture
def user_client(user):
    return login(APIClient(), user.username)


@pytest.fixture
def admin_client(admin_user):
    return login(APIClient(), admin_user.username)


@pytest.fixture
def category():
    return Category.objects.create(name="Вечірка")


@pytest.fixture
def organizer():
    return Organizer.objects.create(name="Kyiv-Mohyla Party Crew")


@pytest.fixture
def venue():
    return Venue.objects.create(
        name="Лофт «Цех»",
        type="loft",
        district="Поділ",
        address="вул. Кирилівська, 41",
        capacity=200,
    )


@pytest.fixture
def event(category, organizer, venue):
    return Event.objects.create(
        title="Посвята першокурсників",
        description="Головна вечірка осені.",
        starts_at="2026-12-12T21:00:00+02:00",
        entry_type="free",
        capacity=150,
        category=category,
        organizer=organizer,
        venue=venue,
    )


@pytest.fixture
def event_data(category, organizer, venue):
    return {
        "title": "Благодійна вечірка",
        "description": "Усі донати йдуть на збір.",
        "starts_at": "2026-12-19T21:00:00+02:00",
        "ends_at": "2026-12-20T03:00:00+02:00",
        "entry_type": "donation",
        "price": 0,
        "min_donation": 100,
        "fundraising_url": "https://example.com/jar",
        "capacity": 100,
        "category": category.id,
        "organizer": organizer.id,
        "venue": venue.id,
    }
