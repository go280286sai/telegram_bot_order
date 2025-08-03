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
async def test_create_carousel(client: AsyncClient, monkeypatch):
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
async def test_carousel_success(client: AsyncClient, monkeypatch):
    # Send login and password
    response_user = await client.post("/user/login",
                                      json={
                                          "username": "User",
                                          "password": "qwertyQWERTY0!"
                                      })
    assert response_user.status_code == 200
    data = response_user.json()
    assert data['success'] is True
    # Create a new carousel
    response = await client.post("/front/carousel/create", json={
        "title": "Title",
        "description": "Description",
        "image": "Image"
    })
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data'] is None
    assert data['error'] is None
    # Update carousel
    response = await client.post("/front/carousel/update/1",
                                 headers={
                                     "Content-Type": "application/json"
                                 },
                                 json={
                                     "title": "Title2",
                                     "description": "Description2",
                                     "image": "Image2"
                                 })
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data'] is None
    assert data['error'] is None
    # Get carousel
    response = await client.get(
        "http://127.0.0.1:8000/front/carousel/gets")
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    for carousel in data['data']['carousels']:
        assert carousel['id'] == 1
        assert carousel['title'] == "Title2"
        assert carousel['description'] == "Description2"
        assert carousel['image'] == "Image2"
    assert data['error'] is None
    # Delete carousel
    response = await client.post("/front/carousel/delete/1")
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data'] is None
    assert data['error'] is None


@pytest.mark.asyncio
async def test_carousel_permission_denied(client: AsyncClient, monkeypatch):
    # Send login and password
    response_user = await client.post("/user/login",
                                      json={
                                          "username": "User1",
                                          "password": "qwertyQWERTY0!"
                                      })
    assert response_user.status_code == 200
    data = response_user.json()
    assert data['success'] is True
    # Create a new carousel
    response = await client.post("/front/carousel/create", json={
        "title": "Title",
        "description": "Description",
        "image": "Image"
    })
    assert response.status_code == 403
    data = response.json()
    assert data['success'] is False
    assert data['data'] is None
    assert data['error'] == "Permission denied"
    # Update carousel
    response = await client.post("/front/carousel/update/1",
                                 headers={
                                     "Content-Type": "application/json"
                                 },
                                 json={
                                     "title": "Title2",
                                     "description": "Description2",
                                     "image": "Image2"
                                 })
    assert response.status_code == 403
    data = response.json()
    assert data['success'] is False
    assert data['data'] is None
    assert data['error'] == "Permission denied"
    # Get carousel
    response = await client.get(
        "http://127.0.0.1:8000/front/carousel/gets")
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data'] is not None
    assert data['error'] is None
    # Delete carousel
    response = await client.post("/front/carousel/delete/1")
    assert response.status_code == 403
    data = response.json()
    assert data['success'] is False
    assert data['data'] is None
    assert data['error'] == "Permission denied"


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
