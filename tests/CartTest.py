import sys

sys.path.append("D:/dev/python/projects/bot_order")
import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_add_to_cart_sets_cookie():
    product_id = 1

    async with AsyncClient(base_url="http://127.0.0.1:8000", cookies={}) as client:
        response = await client.post(f"/cart/add/{product_id}")

    assert response.status_code == 200
    assert response.json() == {"cart": {"1": 1}}
    assert "set-cookie" in response.headers
    assert "cart=" in response.headers["set-cookie"]
    assert response.json().get("cart")['1'] == product_id


@pytest.mark.asyncio
async def test_remove_from_cart_sets_cookie():
    product_id = 1
    async with AsyncClient(base_url="http://127.0.0.1:8000", cookies={}) as client:
        response = await client.post(f"/cart/add/{product_id}")
    assert response.json().get("cart")['1'] == product_id

    async with AsyncClient(base_url="http://127.0.0.1:8000", cookies={}) as client:
        response = await client.post(f"/cart/remove/{product_id}")
    assert response.status_code == 200
    assert response.json() == {"cart": {}}
    assert "set-cookie" in response.headers
    assert "cart=" in response.headers["set-cookie"]
    assert response.json().get("cart") == {}

@pytest.mark.asyncio
async def test_get_from_cart_sets_cookie():
    product_id = 1
    async with AsyncClient(base_url="http://127.0.0.1:8000", cookies={}) as client:
        response = await client.post(f"/cart/add/{product_id}")
    assert response.json().get("cart")['1'] == product_id

    async with AsyncClient(base_url="http://127.0.0.1:8000", cookies={}, params={'credentials': "include"}) as client:
        response = await client.get(f"/cart", )
    assert response.status_code == 200

