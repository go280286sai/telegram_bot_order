import pytest
from dataclasses import dataclass

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
                                         "password": "qwertyQWERTY0!",
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
        assert response.status_code == 422
        data = response.json()
        assert data['success'] is False


@pytest.mark.asyncio
async def test_is_auth():
    async with AsyncClient(
            transport=transport,
            base_url='http://localhost:8000',
            cookies={"user_id": "1"}
    ) as client:
        response = await client.post("/user/is_auth")
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert data['data'] is not None
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
                                         "password": "qwertyQWERTY0!"
                                     })
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        response = await client.post("/user/login",
                                     json={
                                         "username": "User1",
                                         "password": "qwertyQWERTY0!"
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
async def test_delete_user_profile(monkeypatch):
    async with AsyncClient(
            transport=transport,
            base_url='http://localhost:8000',
            cookies={"user_id": "1"}
    ) as client:
        async def mock_set_hashed_active_for_delete(self, *args, **kwargs):
            return "admin@admin.com"

        def mock_add_task(self, *args, **kwargs):
            return

        from routers.UserRouter import UserManager
        monkeypatch.setattr(
            UserManager,
            "set_hashed_active_for_delete",
            mock_set_hashed_active_for_delete
        )
        from routers.UserRouter import BackgroundTasks
        monkeypatch.setattr(BackgroundTasks, "add_task", mock_add_task)
        response = await client.post("/user/delete_user")
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert data['data'] is None
        assert data['error'] is None


@pytest.mark.asyncio
async def test_delete_confirm_user_profile(monkeypatch):
    async with AsyncClient(
            transport=transport,
            base_url='http://localhost:8000'
    ) as client:
        @dataclass
        class User:
            hashed_active: str

        async def mock_get_user(self, *args, **kwargs):
            return User(hashed_active="qwerty")

        async def mock_delete_user(self, *args, **kwargs):
            return True

        async def mock_confirm_delete_user(*args, **kwargs):
            return True

        from routers.UserRouter import UserManager
        monkeypatch.setattr(UserManager, 'get_user', mock_get_user)
        monkeypatch.setattr(UserManager, "delete_user", mock_delete_user)
        monkeypatch.setattr(
            "routers.UserRouter.confirm_delete_user",
            mock_confirm_delete_user
        )
        response = await client.get("/user/delete_confirm/1/qwerty")
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
async def test_delete_user(monkeypatch):
    async with AsyncClient(
            transport=transport,
            base_url='http://localhost:8000',
            cookies={"user_id": "1"}
    ) as client:
        async def mock_is_admin(self, *args, **kwargs):
            return True

        monkeypatch.setattr("routers.UserRouter.is_admin", mock_is_admin)
        response = await client.post("/user/delete/1")
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert data['data'] is None
        assert data['error'] is None
