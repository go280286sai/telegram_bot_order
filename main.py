import asyncio
import logging
import os

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from routers import (cart_router, user_router, order_router, logs_router, front_router, product_router, review_router,
                     post_router, city_router, address_router, subscriber_router, template_router, setting_router)
from database.main import engine, Base
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename="logs.log", filemode='a+', datefmt='%d-%m-%y %H:%M:%S'
)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


asyncio.run(init_db())

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware,
    secret_key="123456789"
)
app.include_router(cart_router.router, prefix="/cart", tags=["Carts"])
app.include_router(user_router.router, prefix="/user", tags=["Users"])
app.include_router(order_router.router, prefix="/order", tags=["Orders"])
app.include_router(logs_router.router, prefix="/logs", tags=["Logs"])
app.include_router(front_router.router, prefix="/front", tags=["Fronts"])
app.include_router(product_router.router, prefix="/product", tags=["Products"])
app.include_router(review_router.router, prefix="/review", tags=["Reviews"])
app.include_router(post_router.router, prefix="/post", tags=["Posts"])
app.include_router(city_router.router, prefix="/city", tags=["Cities"])
app.include_router(address_router.router, prefix="/address", tags=["Addresses"])
app.include_router(subscriber_router.router, prefix="/subscriber", tags=["Subscribers"])
app.include_router(template_router.router, prefix="/template", tags=["Templates"])
app.include_router(setting_router.router, prefix="/setting", tags=["Settings"])

app.mount("/static", StaticFiles(directory="frontend/build/static"), name="static")

# Catch-all
@app.get("/{full_path:path}")
async def serve_react_app(full_path: str):
    file_path = os.path.join("frontend/build", "index.html")
    return FileResponse(file_path)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
