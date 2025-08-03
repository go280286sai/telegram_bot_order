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
async def test_create_review(client: AsyncClient, monkeypatch):
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
async def test_review_success(client: AsyncClient, monkeypatch):
    # Send login and password
    response_user = await client.post("/user/login",
                                      json={
                                          "username": "User",
                                          "password": "qwertyQWERTY0!"
                                      })
    assert response_user.status_code == 200
    data = response_user.json()
    assert data['success'] is True
    # Create a new review
    response = await client.post("/review/create",
                                 headers={
                                     "Content-Type": "application/json"
                                 },
                                 json={
                                     "name": "Author",
                                     "text": "Description",
                                     "gender": 0
                                 })
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data'] is None
    assert data['error'] is None
    # Update reviews
    response = await client.post("/review/update/1",
                                 headers={
                                     "Content-Type": "application/json"
                                 },
                                 json={
                                     "name": "Author2",
                                     "text": "Description2",
                                     "gender": 1
                                 })
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data'] is None
    assert data['error'] is None
    # Get reviews
    response = await client.get("/review/reviews")
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    for review in data['data']['reviews']:
        assert review['id'] == 1
        assert review['name'] == "Author2"
        assert review['text'] == "Description2"
        assert review['gender'] == 1
    assert data['error'] is None
    # Delete reviews
    response = await client.post("/review/delete/1")
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data'] is None
    assert data['error'] is None


@pytest.mark.asyncio
async def test_review_fail(client: AsyncClient, monkeypatch):
    # Send login and password
    response_user = await client.post("/user/login",
                                      json={
                                          "username": "User1",
                                          "password": "qwertyQWERTY0!"
                                      })
    assert response_user.status_code == 200
    data = response_user.json()
    assert data['success'] is True
    # Create a new review
    response = await client.post("/review/create",
                                 headers={
                                     "Content-Type": "application/json"
                                 },
                                 json={
                                     "name": "Author",
                                     "text": "Description",
                                     "gender": 0
                                 })
    assert response.status_code == 403
    data = response.json()
    assert data['success'] is False
    assert data['data'] is None
    assert data['error'] == "Permission denied"
    # Update reviews
    response = await client.post("/review/update/1",
                                 headers={
                                     "Content-Type": "application/json"
                                 },
                                 json={
                                     "name": "Author2",
                                     "text": "Description2",
                                     "gender": 1
                                 })
    assert response.status_code == 403
    data = response.json()
    assert data['success'] is False
    assert data['data'] is None
    assert data['error'] == "Permission denied"
    # Get reviews
    response = await client.get("/review/reviews")
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data'] is not None
    assert data['error'] is None
    # Delete reviews
    response = await client.post("/review/delete/1")
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
