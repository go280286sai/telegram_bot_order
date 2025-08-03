import pytest
from httpx import AsyncClient, ASGITransport
from main import app
import pytest_asyncio

transport = ASGITransport(app=app)


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(
            transport=transport,
            base_url="http://test"
    ) as client:
        yield client


@pytest.mark.asyncio
async def test_create_user(client: AsyncClient, monkeypatch):
    def mock_background_task(*args, **kwargs):
        return True

    monkeypatch.setattr(
        "routers.user_router.BackgroundTasks.add_task",
        mock_background_task
    )
    response = await client.post("/user/register",
                                 json={
                                     "username": "User",
                                     "password": "qwertyQWERTY0!",
                                     "email": "admin@admin.ua",
                                     "phone": "+55555555555"
                                 })
    assert response.status_code == 200
    data_user = response.json()
    assert data_user['success'] is True
    assert data_user['data']['user']['is_admin'] == "1"
    assert data_user['error'] is False
    response = await client.post("/user/register",
                                 json={
                                     "username": "User1",
                                     "password": "qwertyQWERTY0!",
                                     "email": "admin1@admin.ua",
                                     "phone": "+555555555551"
                                 })
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['user']['is_admin'] == "0"


@pytest.mark.asyncio
async def test_setting_fail(client: AsyncClient, monkeypatch):
    # Send login and password
    response_user = await client.post("/user/login",
                                      json={
                                          "username": "User1",
                                          "password": "qwertyQWERTY0!"
                                      })
    assert response_user.status_code == 200
    data = response_user.json()
    assert data['success'] is True
    # Create a new setting
    payload = {"name": "Title", "value": "Value"}
    response = await client.post("/setting/create", json=payload)
    assert response.status_code == 403
    data = response.json()
    assert data['success'] is False
    assert data['data'] is None
    assert data['error'] == "Permission denied"
    # Update setting
    payload = {"name": "Title2", "value": "Value2"}
    response = await client.post("/setting/update/1", json=payload)
    assert response.status_code == 403
    data = response.json()
    assert data['success'] is False
    assert data['data'] is None
    assert data['error'] == "Permission denied"
    # Gets settings
    response = await client.get("/setting/gets")
    assert response.status_code == 403
    data = response.json()
    assert data['success'] is False
    assert data['data'] is None
    assert data['error'] == "Permission denied"
    # Auto create
    response = await client.post("/setting/auto_create")
    assert response.status_code == 403
    data = response.json()
    assert data['success'] is False
    assert data['data'] is None
    assert data['error'] == "Permission denied"
    # Get discount
    response = await client.get("/setting/get/discount")
    assert response.status_code == 400
    # Truncate
    response = await client.post("/setting/truncates")
    assert response.status_code == 403
    data = response.json()
    assert data['success'] is False
    assert data['data'] is None
    assert data['error'] == "Permission denied"


@pytest.mark.asyncio
async def test_setting_success(client: AsyncClient, monkeypatch):
    # Send login and password
    response_user = await client.post("/user/login",
                                      json={
                                          "username": "User",
                                          "password": "qwertyQWERTY0!"
                                      })
    assert response_user.status_code == 200
    data = response_user.json()
    assert data['success'] is True
    # Create a new setting
    payload = {"name": "Title", "value": "Value"}
    response = await client.post("/setting/create", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data'] is None
    assert data['error'] is None
    # Update setting
    payload = {"name": "Title2", "value": "Value2"}
    response = await client.post("/setting/update/1", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data'] is None
    assert data['error'] is None
    # Gets settings
    response = await client.get("/setting/gets")
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    for item in data['data']['settings']:
        assert item['id'] > 0
        assert item['name'] in [
            "Title", "Title2", "title",
            "description", "email",
            "telegram", "phone",
            "viber", "whatsapp",
            "map", "promotional",
            "address", "discount"]
    assert data['error'] is None
    # Delete setting
    response = await client.get("/setting/gets")
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    for item in data['data']['settings']:
        response = await client.post(f"/setting/delete/{item['id']}")
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert data['data'] is None
        assert data['error'] is None
    # Auto create
    response = await client.post("/setting/auto_create")
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data'] is None
    assert data['error'] is None
    # Get discount
    response = await client.get("/setting/get/discount")
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    # Truncate
    response = await client.post("/setting/truncates")
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data'] is None
    assert data['error'] is None
