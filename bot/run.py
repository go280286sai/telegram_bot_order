from dotenv import load_dotenv

load_dotenv()
import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import BotCommand, Message, CallbackQuery

bot = Bot(str(os.getenv("BOT_KEY")), parse_mode='HTML')
dp = Dispatcher()


@dp.message(CommandStart())
async def echo(message: Message):
    await message.answer("ok")


async def start_bot():
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        print("Starting bot...")
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        print("Shutting down")