import asyncio
import logging
from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from routers import CartRouter, UserRouter, OrderRouter
from database.main import engine, Base

app = FastAPI()
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename="logs.log", filemode='w', datefmt='%d-%m-%y %H:%M:%S'
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
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(CartRouter.router, prefix="/cart", tags=["Carts"])
app.include_router(UserRouter.router, prefix="/user", tags=["Users"])
app.include_router(OrderRouter.router, prefix="/order", tags=["Orders"])


@app.get("/")
async def index():
    return {"Hello": "World"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
