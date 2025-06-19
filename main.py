import asyncio
import json
from typing import List, Dict

from fastapi import FastAPI, Cookie, Response, Request
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from database.Products import ProductManager
from database.main import get_db, engine, Base, async_session_maker
app = FastAPI()


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


asyncio.run(init_db())
origins = [
    "http://localhost:3000",  # React по умолчанию
    "http://127.0.0.1:3000"
]

# Добавление middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Разрешённые домены
    allow_credentials=True,
    allow_methods=["*"],              # Разрешённые методы (GET, POST и т.д.)
    allow_headers=["*"],              # Разрешённые заголовки
)


@app.get("/")
async def index():
    return {"Hello": "World"}

@app.get("/products")
async def products():
    async with async_session_maker() as session:
        product_manager = ProductManager(session)
        products = await product_manager.get_products()
        return {"products": products}

@app.post("/cart/add/{product_id}")
async def add_to_cart(product_id: int, response: Response, cart: str = Cookie(default="{}")):
    try:
        cart_items = json.loads(cart)
        if not isinstance(cart_items, dict):
            cart_items = {}
    except json.JSONDecodeError:
        cart_items = {}

    # Преобразуем ключи в int
    cart_items = {int(k): v for k, v in cart_items.items()}

    # Увеличиваем количество, если уже есть
    if product_id in cart_items:
        cart_items[product_id] += 1
    else:
        cart_items[product_id] = 1

    # Преобразуем обратно в строковый JSON со строковыми ключами
    cookie_value = json.dumps({str(k): v for k, v in cart_items.items()})

    response.set_cookie(key="cart", value=cookie_value, httponly=True)
    return {"cart": cart_items}

@app.post("/cart/increase/{product_id}")
async def increase_amount(product_id: int, response: Response, cart: str = Cookie(default="{}")):
    try:
        cart_items = json.loads(cart)
        if not isinstance(cart_items, dict):
            cart_items = {}
    except json.JSONDecodeError:
        cart_items = {}

    cart_items = {int(k): v for k, v in cart_items.items()}

    if product_id in cart_items:
        cart_items[product_id] += 1
    else:
        cart_items[product_id] = 1

    response.set_cookie(
        key="cart",
        value=json.dumps({str(k): v for k, v in cart_items.items()}),
        httponly=True
    )
    return {"cart": cart_items}
@app.post("/cart/decrease/{product_id}")
async def decrease_amount(product_id: int, response: Response, cart: str = Cookie(default="{}")):
    try:
        cart_items = json.loads(cart)
        if not isinstance(cart_items, dict):
            cart_items = {}
    except json.JSONDecodeError:
        cart_items = {}

    cart_items = {int(k): v for k, v in cart_items.items()}

    if product_id in cart_items:
        if cart_items[product_id] > 1:
            cart_items[product_id] -= 1
        else:
            del cart_items[product_id]  # удаляем, если количество стало 0

    response.set_cookie(
        key="cart",
        value=json.dumps({str(k): v for k, v in cart_items.items()}),
        httponly=True
    )
    return {"cart": cart_items}

@app.post("/cart/remove/{product_id}")
async def remove_from_cart(product_id: int, response: Response, cart: str = Cookie(default="{}")):
    cart_items = json.loads(cart)
    if product_id in cart_items:
        del cart_items[product_id]
    response.set_cookie(key="cart", value=json.dumps(cart_items), httponly=True)
    return {"cart": cart_items}

@app.get("/cart")
async def get_cart(request: Request):
    raw_cart_cookie = request.cookies.get("cart")
    cart_items: Dict[int, int] = {}

    if raw_cart_cookie:
        try:
            cart_items = json.loads(raw_cart_cookie)
            cart_items = {int(k): v for k, v in cart_items.items()}
        except json.JSONDecodeError:
            cart_items = {}

    async with async_session_maker() as session:
        product_manager = ProductManager(session)
        products = []
        for product_id, amount in cart_items.items():
            product = await product_manager.get_product(product_id)
            if product:
                product_data = product.to_dict() if hasattr(product, "to_dict") else {
                    "id": product.id,
                    "name": product.name,
                    "price": product.price,
                    "description": product.description,
                    "amounts": product.amount,
                }
                product_data["amount"] = amount
                products.append(product_data)

    return {"cart": products}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
