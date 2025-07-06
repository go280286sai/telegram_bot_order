import pytest
from httpx import AsyncClient, ASGITransport
from main import app
from helps import emails
from database.Subscriber import SubscriberManager


@pytest.mark.asyncio
async def test_create_valid_subscriber(monkeypatch):
    async def mock_create_subscriber_email(idx, email, hash_active):
        return True

    class DummySubscriber:
        def __init__(self, id):
            self.id = id

    async def mock_create_subscriber(self, email, hash_active):
        return DummySubscriber(id=1)

    monkeypatch.setattr(
        emails,
        "create_subscriber_email",
        mock_create_subscriber_email
    )
    monkeypatch.setattr(
        SubscriberManager,
        "create_subscriber",
        mock_create_subscriber
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(
            transport=transport,
            base_url="http://test"
    ) as ac:
        payload = {"email": "test@example.com"}
        response = await ac.post("/subscriber/create", json=payload)

    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "data": None,
        "error": None
    }


@pytest.mark.asyncio
async def test_create_invalid_email():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        payload = {"email": "not-an-email"}
        response = await ac.post("/subscriber/create", json=payload)

    assert response.status_code == 422
    assert response.json()["error"] == "Invalid email format"


@pytest.mark.asyncio
async def test_create_duplicate_email(monkeypatch):
    async def mock_create_subscriber(email, hash_active):
        raise Exception("Email already exists")

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        from database.Subscriber import SubscriberManager
        monkeypatch.setattr(
            SubscriberManager,
            "create_subscriber",
            mock_create_subscriber
        )

        payload = {"email": "test@example.com"}
        response = await ac.post("/subscriber/create", json=payload)

    assert response.status_code == 400
    assert response.json()["error"] == "Failed to confirm subscriber"


@pytest.mark.asyncio
async def test_confirm_email(monkeypatch):
    async def mock_set_active_subscriber(self, idx, hash_active):
        return True

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        from database.Subscriber import SubscriberManager
        monkeypatch.setattr(
            SubscriberManager,
            "set_active_subscriber",
            mock_set_active_subscriber
        )
        response = await ac.get("/subscriber/confirm/1/dfgdf")
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_destroy_email(monkeypatch):
    async def mock_set_destroy_subscriber(self, idx, hash_destroy):
        return True

    from database.Subscriber import SubscriberManager
    monkeypatch.setattr(
        SubscriberManager,
        "set_destroy_subscriber",
        mock_set_destroy_subscriber
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/subscriber/destroy/1/dfgdf")
        assert response.status_code == 200
