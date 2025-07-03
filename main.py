import asyncio
import logging
from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from routers import CartRouter, UserRouter, OrderRouter, LogsRouter, FrontRouter, ProductRouter, ReviewRouter, \
    DeliveryRouter, PostRouter, CityRouter, AddressRouter
from database.main import engine, Base
from starlette.middleware.sessions import SessionMiddleware
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
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware,
    secret_key="123456789"  # только для session middleware
)
app.include_router(CartRouter.router, prefix="/cart", tags=["Carts"])
app.include_router(UserRouter.router, prefix="/user", tags=["Users"])
app.include_router(OrderRouter.router, prefix="/order", tags=["Orders"])
app.include_router(LogsRouter.router, prefix="/logs", tags=["Logs"])
app.include_router(FrontRouter.router, prefix="/front", tags=["Fronts"])
app.include_router(ProductRouter.router, prefix="/product", tags=["Products"])
app.include_router(ReviewRouter.router, prefix="/review", tags=["Reviews"])
app.include_router(PostRouter.router, prefix="/post", tags=["Posts"])
app.include_router(CityRouter.router, prefix="/city", tags=["Cities"])
app.include_router(AddressRouter.router, prefix="/address", tags=["Addresses"])
app.include_router(DeliveryRouter.router, prefix="/delivery", tags=["Deliveries"])


@app.get("/")
async def index():
    return {"Hello": "World"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
