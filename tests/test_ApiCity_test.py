import pytest
from main import app
from httpx import AsyncClient, ASGITransport
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
async def test_city_success(client: AsyncClient, monkeypatch):
    # Send login and password
    response_user = await client.post("/user/login",
                                      json={
                                          "username": "User",
                                          "password": "qwertyQWERTY0!"
                                      })
    assert response_user.status_code == 200
    data = response_user.json()
    assert data['success'] is True
    # Create a new city
    response = await client.post("/city/create",
                                 json={
                                     "name": "Title",
                                     "post_id": 1
                                 })
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data'] is None
    assert data['error'] is None
    # Update city
    response = await client.post("/city/update/1",
                                 json={
                                     "name": "Title2",
                                     "post_id": 2,
                                 })
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data'] is None
    assert data['error'] is None
    # Get city
    response = await client.get("/city/get/1")
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    for item in data['data']["cities"]:
        assert item['id'] == 1
        assert item['name'] == "Title2"
        assert item['post_id'] == 2
    assert data['error'] is None
    # Delete city
    responses = await client.get("/city/gets")
    data = responses.json()
    for item in data['data']['cities']:
        response = await client.post(f"/city/delete/{item['id']}")
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert data['data'] is None
        assert data['error'] is None


@pytest.mark.asyncio
async def test_city_permission_denied(client: AsyncClient, monkeypatch):
    # Send login and password
    response_user = await client.post("/user/login",
                                      json={
                                          "username": "User1",
                                          "password": "qwertyQWERTY0!"
                                      })
    assert response_user.status_code == 200
    data = response_user.json()
    assert data['success'] is True
    # Create a new city
    response = await client.post("/city/create",
                                 json={
                                     "name": "Title",
                                     "post_id": 1
                                 })
    assert response.status_code == 403
    data = response.json()
    assert data['success'] is False
    assert data['data'] is None
    assert data['error'] == "Permission denied"
    # Update city
    response = await client.post("/city/update/1",
                                 json={
                                     "name": "Title2",
                                     "post_id": 2,
                                 })
    assert response.status_code == 403
    data = response.json()
    assert data['success'] is False
    assert data['data'] is None
    assert data['error'] == "Permission denied"
    # Get city
    response = await client.get("/city/get/1")
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data'] is not None
    assert data['error'] is None
    # Delete city
    responses = await client.get("/city/gets")
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
    # Create a new city
    response = await client.post("/city/create",
                                 json={
                                     "name": "Title",
                                     "post_id": 0
                                 })
    assert response.status_code == 400
    data = response.json()
    assert data['success'] is False
    assert data['data'] is None
    assert data['error'] == "Failed to create city"
    # Update city
    response = await client.post("/city/update/0",
                                 json={
                                     "name": "Title2",
                                     "post_id": 2,
                                 })
    assert response.status_code == 400
    data = response.json()
    assert data['success'] is False
    assert data['data'] is None
    assert data['error'] == "Failed to update city"
    # Get city
    response = await client.get("/city/get/0")
    assert response.status_code == 400
    data = response.json()
    assert data['success'] is False
    assert data['data'] is None
    assert data['error'] == "Failed to fetch cities"
    # Delete city
    response = await client.post("/city/delete/0")
    assert response.status_code == 400
    data = response.json()
    assert data['success'] is False
    assert data['data'] is None
    assert data['error'] == "Failed to delete city"


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
