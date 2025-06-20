import json
import sys

sys.path.append("D:/dev/python/projects/bot_order")
import pytest
from httpx import AsyncClient
from fastapi import status


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


@pytest.mark.asyncio
async def test_cart_increase_and_decrease():
    # Начальный пустой cookie
    cart_cookie = json.dumps({"1": 1})  # товар с id=1 в количестве 1

    async with AsyncClient(base_url="http://127.0.0.1:8000") as ac:
        # Увеличиваем количество
        response_increase = await ac.post(
            "/cart/increase/1",
            cookies={"cart": cart_cookie}
        )
        assert response_increase.status_code == status.HTTP_200_OK
        assert response_increase.json()["cart"]["1"] == 2

        # Уменьшаем количество
        response_decrease = await ac.post(
            "/cart/decrease/1",
            cookies={"cart": json.dumps({"1": 2})}
        )
        assert response_decrease.status_code == status.HTTP_200_OK
        assert response_decrease.json()["cart"]["1"] == 1

        # Удаляем товар при уменьшении до 0
        response_remove = await ac.post(
            "/cart/decrease/1",
            cookies={"cart": json.dumps({"1": 1})}
        )
        assert response_remove.status_code == status.HTTP_200_OK
        assert "1" not in response_remove.json()["cart"]
