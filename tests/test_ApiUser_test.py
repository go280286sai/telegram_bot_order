import pytest

from main import app
from httpx import AsyncClient, ASGITransport

transport = ASGITransport(app=app)


@pytest.mark.asyncio
async def test_create_api_city():
    async with AsyncClient(
            transport=transport,
            base_url='http://localhost:8000'
    ) as client:
        response = await client.post("/user/register",
                                     json={
                                         "username": "User",
                                         "password": "qweqqwRerw44",
                                         "email": "admin@admin.ua",
                                         "phone": "+55555555555"
                                     })
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert data['data'] is None
        assert data['error'] is None
        response = await client.post("/user/register",
                                     json={
                                         "username": "User1",
                                         "password": "0000",
                                         "email": "admin1@admin.ua",
                                         "phone": "+55555555555"
                                     })
        assert response.status_code == 400
        data = response.json()
        assert data['success'] is False


@pytest.mark.asyncio
async def test_is_auth():
    async with AsyncClient(
            transport=transport,
            base_url='http://localhost:8000'
    ) as client:
        response = await client.post("/user/is_auth")
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert data['data'] is None
        assert data['error'] is None


@pytest.mark.asyncio
async def test_login():
    async with AsyncClient(
            transport=transport,
            base_url='http://localhost:8000'
    ) as client:
        response = await client.post("/user/login",
                                     json={
                                         "username": "User",
                                         "password": "qweqqwRerw44"
                                     })
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        response = await client.post("/user/login",
                                     json={
                                         "username": "User1",
                                         "password": "qweqqwRerw44"
                                     })
        assert response.status_code == 400
        data = response.json()
        assert data['success'] is False
        response = await client.post("/user/login",
                                     json={
                                         "username": "User",
                                         "password": "qweqqwRerw443"
                                     })
        assert response.status_code == 400
        data = response.json()
        assert data['success'] is False


@pytest.mark.asyncio
async def test_logout():
    async with AsyncClient(
            transport=transport,
            base_url='http://localhost:8000'
    ) as client:
        response = await client.post("/user/logout")
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True


@pytest.mark.asyncio
async def test_update_profile():
    async with AsyncClient(
            transport=transport,
            base_url='http://localhost:8000'
    ) as client:
        response = await client.post("/user/update_profile",
                                     json={
                                         "idx": "1",
                                         "password": "qwertyASD123",
                                     })
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        response = await client.post("/user/update_profile",
                                     json={
                                         "idx": "5",
                                         "password": "qwertyASD123",
                                     })
        assert response.status_code == 400
        data = response.json()
        assert data['success'] is False


@pytest.mark.asyncio
async def test_user_confirm(monkeypatch):
    TOKEN = "Cerebra"
    from types import SimpleNamespace

    async def mock_get_user(self, idx):
        return SimpleNamespace(hashed_active=TOKEN)

    async with AsyncClient(
            transport=transport,
            base_url='http://localhost:8000'
    ) as client:
        from database.User import UserManager
        monkeypatch.setattr(UserManager, "get_user", mock_get_user)

        response = await client.get(f"/user/confirm/1/{TOKEN}")
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_user_recover(monkeypatch):
    async with AsyncClient(
            transport=transport,
            base_url='http://localhost:8000'
    ) as client:
        response = await client.post("/user/recovery",
                                     json={
                                         "username": "User",
                                         "email": "admin1@admin.ua"
                                     })
        assert response.status_code == 400
        response = await client.post("/user/recovery",
                                     json={
                                         "username": "User1",
                                         "email": "admin@admin.ua"
                                     })
        assert response.status_code == 400
        response = await client.post("/user/recovery",
                                     json={
                                         "username": "User",
                                         "email": "admin@admin.ua"
                                     })
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_user():
    async with AsyncClient(
            transport=transport,
            base_url='http://localhost:8000'
    ) as client:
        response = await client.post("/user/delete/1")
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
