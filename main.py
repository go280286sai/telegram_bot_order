from dotenv import load_dotenv
load_dotenv()
import os
from fastapi import FastAPI
import uvicorn

import asyncio
from aiogram import Bot, Dispatcher
bot = Bot(os.getenv("BOT_KEY"))
dp = Dispatcher()

@dp.message()


async def main_bot():
    await dp.start_polling(bot)



app = FastAPI()

@app.get("/")
async def main():
    return {"status":"ok"}



if __name__ == "__main__":
    uvicorn.run(app=app, host="127.0.0.1", port=8000)
