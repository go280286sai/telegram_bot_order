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
async def test_address_success(client: AsyncClient, monkeypatch):
    # Send login and password
    response_user = await client.post("/user/login",
                                      json={
                                          "username": "User",
                                          "password": "qwertyQWERTY0!"
                                      })
    assert response_user.status_code == 200
    data = response_user.json()
    assert data['success'] is True
    # Create a new address
    response = await client.post("/address/create",
                                 json={
                                     "name": "Title",
                                     "city_id": 1
                                 })
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data'] is None
    assert data['error'] is None
    # Update address
    response = await client.post("/address/update/1",
                                 json={
                                     "name": "Title2",
                                     "city_id": 2,
                                 })
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data'] is None
    assert data['error'] is None
    # Get address
    response = await client.get("/address/get/1")
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    for item in data['data']["addresses"]:
        assert item['id'] == 1
        assert item['name'] == "Title2"
    assert data['error'] is None
    # Delete addresses
    responses = await client.get("/address/gets")
    data = responses.json()
    for item in data['data']['addresses']:
        response = await client.post(f"/address/delete/{item['id']}")
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert data['data'] is None
        assert data['error'] is None


@pytest.mark.asyncio
async def test_address_permission_denied(client: AsyncClient, monkeypatch):
    # Send login and password
    response_user = await client.post("/user/login",
                                      json={
                                          "username": "User1",
                                          "password": "qwertyQWERTY0!"
                                      })
    assert response_user.status_code == 200
    data = response_user.json()
    assert data['success'] is True
    # Create a new address
    response = await client.post("/address/create",
                                 json={
                                     "name": "Title",
                                     "city_id": 1
                                 })
    assert response.status_code == 403
    data = response.json()
    assert data['success'] is False
    assert data['data'] is None
    assert data['error'] == "Permission denied"
    # Update address
    response = await client.post("/address/update/1",
                                 json={
                                     "name": "Title2",
                                     "city_id": 2,
                                 })
    assert response.status_code == 403
    data = response.json()
    assert data['success'] is False
    assert data['data'] is None
    assert data['error'] == "Permission denied"
    # Get address
    response = await client.get("/address/get/1")
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data'] is not None
    assert data['error'] is None
    # Delete addresses
    responses = await client.get("/address/gets")
    assert responses.status_code == 200
    data = responses.json()
    assert data['success'] is True
    assert data['data'] is not None
    assert data['error'] is None


@pytest.mark.asyncio
async def test_address_fail(client: AsyncClient, monkeypatch):
    # Send login and password
    response_user = await client.post("/user/login",
                                      json={
                                          "username": "User",
                                          "password": "qwertyQWERTY0!"
                                      })
    assert response_user.status_code == 200
    data = response_user.json()
    assert data['success'] is True
    # Create a new address
    response = await client.post("/address/create",
                                 json={
                                     "name": "Title",
                                     "city_id": 0
                                 })
    assert response.status_code == 400
    data = response.json()
    assert data['success'] is False
    assert data['data'] is None
    assert data['error'] == "Create address failed"
    # Update address
    response = await client.post("/address/update/0",
                                 json={
                                     "name": "Title2",
                                     "city_id": 2,
                                 })
    assert response.status_code == 400
    data = response.json()
    assert data['success'] is False
    assert data['data'] is None
    assert data['error'] == "Failed to update address"
    # Get address
    response = await client.get("/address/get/0")
    assert response.status_code == 400
    data = response.json()
    assert data['success'] is False
    assert data['data'] is None
    assert data['error'] == "Failed to fetch address"
    # Delete addresses
    response = await client.post("/address/delete/0")
    assert response.status_code == 400
    data = response.json()
    assert data['success'] is False
    assert data['data'] is None
    assert data['error'] == "Failed to delete address"


@pytest.mark.asyncio
async def test_delete_users(client: AsyncClient, monkeypatch):
    response_user = await client.post("/user/login",
                                      json={
                                          "username": "User",
                                          "password": "qwertyQWERTY0!"
                                      })
    assert response_user.status_code == 200
    data = response_user.json()
    assert data['success'] is True
    response_user = await client.post("/user/delete/2")
    assert response_user.status_code == 200
    response_user = await client.post("/user/delete/1")
    assert response_user.status_code == 200
