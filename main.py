import asyncio

from fastapi import FastAPI
import uvicorn
from database.main import get_db, engine, Base

app = FastAPI()

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(init_db())

# @app.post("/register/")
# async def register(username: str, password: str, user_manager: UserManager = Depends(get_user_manager)):
#     user = await user_manager.create_user(username, password)
#     return {"message": "Пользователь зарегистрирован", "user": user.username}
#
# @app.get("/user/{username}")
# async def get_user(username: str, user_manager: UserManager = Depends(get_user_manager)):
#     user = await user_manager.get_user(username)
#     if user:
#         return {"username": user.username, "password": user.password}
#     return {"message": "Пользователь не найден"}
@app.get("/")
async def index():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

