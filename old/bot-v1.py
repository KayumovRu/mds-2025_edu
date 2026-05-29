# простейшая версия ТГ-бота

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message

bot = Bot(token="*******BGmQnHq_f4") # здесь оставлять токен (хардкодить) - это плохо
dp = Dispatcher()

@dp.message()
async def echo_handler(message):
    await message.answer(message.text)

@dp.message()
async def hello_handler(message = "Hi"):
    await message.answer("HELLOOOO")

async def main():
    print("Bot starting...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())