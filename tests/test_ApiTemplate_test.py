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
async def test_template_success(client: AsyncClient, monkeypatch):
    # Send login and password
    response_user = await client.post("/user/login",
                                      json={
                                          "username": "User",
                                          "password": "qwertyQWERTY0!"
                                      })
    assert response_user.status_code == 200
    data = response_user.json()
    assert data['success'] is True
    # Create a new template
    response = await client.post("/template/create",
                                 headers={
                                     "Content-Type": "application/json"
                                 },
                                 json={
                                     "header": "Header",
                                     "title": "Title",
                                     "body": "Body"
                                 })
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data'] is None
    assert data['error'] is None
    # Update template
    response = await client.post("/template/update/1",
                                 headers={
                                     "Content-Type": "application/json"
                                 },
                                 json={
                                     "header": "Header2",
                                     "title": "Title2",
                                     "body": "Body2"
                                 })
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data'] is None
    assert data['error'] is None
    # Get template
    response = await client.post("/template/get/1")
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['templates'][0]["header"] == "Header2"
    assert data['data']['templates'][0]["title"] == "Title2"
    assert data['data']['templates'][0]["body"] == "Body2"
    assert data['error'] is None
    # Gets templates
    response = await client.get("/template/gets")
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    for item in data['data']['templates']:
        assert item["header"] == "Header2"
        assert item["title"] == "Title2"
        assert item["body"] == "Body2"
    assert data['error'] is None
    # Delete city
    response = await client.get("/template/gets")
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    for item in data['data']['templates']:
        response = await client.post(f"/template/delete/{item['id']}")
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert data['data'] is None
        assert data['error'] is None


@pytest.mark.asyncio
async def test_template_permission_denied(client: AsyncClient, monkeypatch):
    response_user = await client.post("/user/login",
                                      json={
                                          "username": "User1",
                                          "password": "qwertyQWERTY0!"
                                      })
    assert response_user.status_code == 200
    # Create a new template
    response_user = await client.post("/template/create",
                                      headers={
                                          "Content-Type": "application/json"
                                      },
                                      json={
                                          "header": "Header",
                                          "title": "Title",
                                          "body": "Body"
                                      })
    assert response_user.status_code == 403
    data = response_user.json()
    assert data['success'] is False
    assert data['data'] is None
    assert data['error'] == "Permission denied"
    # Update template
    response_user = await client.post("/template/update/1",
                                      headers={
                                          "Content-Type": "application/json"
                                      },
                                      json={
                                          "header": "Header2",
                                          "title": "Title2",
                                          "body": "Body2"
                                      })
    assert response_user.status_code == 403
    data = response_user.json()
    assert data['success'] is False
    assert data['data'] is None
    assert data['error'] == "Permission denied"
    # Get template
    response = await client.post("/template/get/1")
    assert response.status_code == 400
    data = response.json()
    assert data['error'] == "No templates"
    # Gets templates
    response = await client.get("/template/gets")
    assert response.status_code == 200
    data = response.json()
    # Delete city
    response = await client.get("/template/gets")
    assert response_user.status_code == 403
    data = response_user.json()
    assert data['success'] is False
    assert data['data'] is None
    assert data['error'] == "Permission denied"


@pytest.mark.asyncio
async def test_template_fail(client: AsyncClient, monkeypatch):
    response_user = await client.post("/user/login",
                                      json={
                                          "username": "User",
                                          "password": "qwertyQWERTY0!"
                                      })
    assert response_user.status_code == 200
    # Create a new template
    response_user = await client.post("/template/create",
                                      headers={
                                          "Content-Type": "application/json"
                                      },
                                      json={
                                          "header": "Header",

                                          "body": "Body"
                                      })
    assert response_user.status_code == 422
    # Update template
    response_user = await client.post("/template/update/0",
                                      headers={
                                          "Content-Type": "application/json"
                                      },
                                      json={
                                          "header": "Header2",
                                          "title": "Title2",
                                          "body": "Body2"
                                      })
    assert response_user.status_code == 400
    data = response_user.json()
    assert data['success'] is False
    assert data['data'] is None
    assert data['error'] == "Failed to update template"
    # Get template
    response = await client.post("/template/get/0")
    assert response.status_code == 400
    data = response.json()
    assert data['error'] == "No templates"
    # Gets templates
    response = await client.get("/template/gets")
    assert response.status_code == 200
    # Delete city
    response_user = await client.get("/template/gets")
    assert response_user.status_code == 200
    data = response_user.json()
    assert data['success'] is True
    assert data['data'] is not None
    assert data['error'] is None


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
