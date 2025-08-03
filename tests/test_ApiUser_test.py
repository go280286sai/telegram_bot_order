import pytest
import pytest_asyncio


from main import app
from httpx import AsyncClient, ASGITransport

transport = ASGITransport(app=app)


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(
            transport=transport,
            base_url="http://test"
    ) as client:
        yield client


@pytest.mark.asyncio
async def test_create_api_user(client: AsyncClient, monkeypatch):
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
                                     "password": "0000",
                                     "email": "admin1@admin.ua",
                                     "phone": "+55555555555"
                                 })
    assert response.status_code == 422
    data = response.json()
    assert data['success'] is False
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
    assert data['error'] is False
    user = data['data']['user']
    response = await client.get(
        f"/user/confirm/{user['id']}/{user['hashed_active']}"
    )
    assert response.status_code == 200
    # Assert is auth
    response = await client.post("/user/is_auth")
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']["id"] == 2
    assert data['error'] is None
    # Delete fail
    response = await client.post("/user/delete/1")
    assert response.status_code == 403
    data = response.json()
    assert data['success'] is False
    assert data['data'] is None
    assert data['error'] == "Permission denied"
    # Logout
    response = await client.post("/user/logout")
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    # Is auth fail
    response = await client.post("/user/is_auth")
    assert response.status_code == 401
    data = response.json()
    assert data['success'] is False
    assert data['data'] is None
    assert data['error'] == "Missing user_id"


@pytest.mark.asyncio
async def test_login(client: AsyncClient, monkeypatch):
    response_user = await client.post("/user/login",
                                      json={
                                          "username": "User",
                                          "password": "qwertyQWERTY0!"
                                      })
    assert response_user.status_code == 200
    data = response_user.json()
    assert data['success'] is True
    response = await client.post("/user/login",
                                 json={
                                     "username": "User2",
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
    response = await client.post("/user/update_profile",
                                 json={
                                     "password": "qwertyQWERTY0!!",
                                 })
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    response = await client.post("/user/update_profile",
                                 json={
                                     "password": "qwerty",
                                 })
    assert response.status_code == 400
    data = response.json()
    assert data['success'] is False
    assert data['error'] == "Invalid password"


@pytest.mark.asyncio
async def test_add_contact(client: AsyncClient, monkeypatch):
    # Input login
    response_user = await client.post("/user/login",
                                      json={
                                          "username": "User",
                                          "password": "qwertyQWERTY0!!"
                                      })
    assert response_user.status_code == 200
    data = response_user.json()
    assert data['success'] is True
    # Set status
    response_user = await client.post("/user/set_status/1/1")
    assert response_user.status_code == 200
    # Get user
    response_user = await client.post("/user/get/1")
    assert response_user.status_code == 200
    data = response_user.json()
    assert data['success'] is True
    assert data['data']['id'] == 1
    assert data['data']['status'] == 1
    assert data['data']['first_name'] is None
    assert data['data']['last_name'] is None
    assert data['data']['email'] == 'admin@admin.ua'
    assert data['data']['comments'] is None
    response_user = await client.post("/user/add_contact_profile",
                                      json={
                                          "first_name": "John",
                                          "last_name": "Doe"
                                      })
    assert response_user.status_code == 200
    data = response_user.json()
    assert data['success'] is True
    response_user = await client.post("/user/update",
                                      json={
                                          "username": "admin",
                                          "email": 'admin@admin.com',
                                          "phone": "+55555555555",
                                          "comments": "Comment",
                                          "first_name": "John",
                                          "last_name": "Doe"
                                      })
    assert response_user.status_code == 200
    data = response_user.json()
    assert data['success'] is True
    response_user = await client.post("/user/get/1")
    assert response_user.status_code == 200
    data = response_user.json()
    assert data['success'] is True
    assert data['data']['id'] == 1
    assert data['data']['first_name'] == "John"
    assert data['data']['last_name'] == "Doe"
    assert data['data']['email'] == 'admin@admin.com'
    assert data['data']['comments'] == "Comment"


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
                                     "username": "Test",
                                     "password": "qwertyQWERTY0!",
                                     "email": "test@admin.ua",
                                     "phone": "+555555555550"
                                 })
    assert response.status_code == 200
    data_user = response.json()
    assert data_user['success'] is True
    assert data_user['data']['user']['is_admin'] == "0"
    assert data_user['error'] is False

    async def mock_reset_password(self, *args, **kwargs):
        return "qwertyQWERTY!!"

    from routers import user_router

    monkeypatch.setattr(user_router.User.UserManager, "reset_password", mock_reset_password)

    response = await client.post("/user/recovery",
                                 json={
                                     "username": "Test",
                                     "email": "test@admin.ua",
                                 })
    assert response.status_code == 200
    data_user = response.json()
    assert data_user['success'] is True

    async def mock_set_hashed_active_for_delete(self, *args, **kwargs):
        return "qwertyQWERTY"

    from routers import user_router
    monkeypatch.setattr(
        user_router.User.UserManager, "set_hashed_active_for_delete",
        mock_set_hashed_active_for_delete
    )
    response = await client.post("/user/delete_user")
    assert response.status_code == 200
    data_user = response.json()
    assert data_user['success'] is True

    async def mock_get_user(self, *args, **kwargs):
        return {"hashed_active": "qwertyQWERTY"}

    from routers import user_router

    monkeypatch.setattr(
        user_router.User.UserManager,"get_user",
        mock_get_user
    )
    response_user = await client.get("/user/delete_confirm/3/qwertyQWERTY")
    assert response_user.status_code == 200


@pytest.mark.asyncio
async def test_delete_contacts(client: AsyncClient, monkeypatch):
    # Input login
    response_user = await client.post("/user/login",
                                      json={
                                          "username": "admin",
                                          "password": "qwertyQWERTY0!!"
                                      })
    assert response_user.status_code == 200
    data = response_user.json()
    assert data['success'] is True
    response_user = await client.post("/user/set_status_admin/2/1")
    assert response_user.status_code == 200
    data = response_user.json()
    assert data['success'] is True
    response_user = await client.post("/user/gets")
    assert response_user.status_code == 200
    data = response_user.json()
    assert data['success'] is True
    results = data['data']['users']
    for item in results:
        if item['id'] != 1:
            response_user = await client.post(f"/user/delete/{item['id']}")
            assert response_user.status_code == 200
    response_user = await client.post("/user/delete/1")
    assert response_user.status_code == 200
