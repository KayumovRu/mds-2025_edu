import asyncio
import logging
import json
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import os

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# Загружаем переменные окружения
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в .env файле!")

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Инициализация бота
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Определение состояний для FSM
class UserStates(StatesGroup):
    waiting_for_bio = State()

# Файл для сохранения био
BIOS_FILE = "user_bios.json"

def load_bios():
    """Загружает существующие био из файла"""
    if Path(BIOS_FILE).exists():
        with open(BIOS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_bio(user_id: int, username: str, bio: str):
    """Сохраняет био в файл"""
    bios = load_bios()
    bios[str(user_id)] = {
        "username": username,
        "bio": bio,
        "saved_at": datetime.now().isoformat()
    }
    with open(BIOS_FILE, 'w', encoding='utf-8') as f:
        json.dump(bios, f, ensure_ascii=False, indent=2)
    logger.info(f"Сохранено био для пользователя {username} (ID: {user_id})")

@dp.message(Command("start"))
async def start_handler(message: Message):
    """Обработчик команды /start"""
    logger.info(f"Новый пользователь: {message.from_user.username} (ID: {message.from_user.id})")
    
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 Написать био", callback_data="write_bio")]
    ])
    
    await message.answer(
        f"Привет, {message.from_user.first_name}! 👋\n\nЯ эхобот с улучшенной версией.\n"
        f"Напиши мне сообщение, и я повторю его, или нажми кнопку ниже.",
        reply_markup=keyboard
    )

@dp.callback_query(F.data == "write_bio")
async def write_bio_callback(
    callback: CallbackQuery,
    state: FSMContext
):
    """Обработчик нажатия кнопки 'Написать био'"""
    logger.info(f"{callback.from_user.username} нажал кнопку 'Написать био'")
    
    await callback.message.answer("✍️ Напиши своё био (не более 500 символов):")
    await state.set_state(UserStates.waiting_for_bio)
    await callback.answer()

@dp.message(UserStates.waiting_for_bio)
async def receive_bio(message: Message, state: FSMContext):
    """Получение био от пользователя"""
    bio = message.text
    
    if len(bio) > 500:
        await message.answer("❌ Био слишком длинное! Максимум 500 символов. Попробуй ещё раз:")
        return
    
    save_bio(
        user_id=message.from_user.id,
        username=message.from_user.username or "Без имени",
        bio=bio
    )
    
    await message.answer("✅ Спасибо! Твоё био сохранено.")
    await state.clear()

@dp.message(F.text == "hello")
async def hello_handler(message: Message):
    """Обработчик команды 'hello'"""
    logger.info(f"{message.from_user.username} написал 'hello'")
    await message.answer("HI!!!!!!!")


@dp.message()
async def echo_handler(message: Message):
    """Эхо-обработчик для всех остальных сообщений"""
    logger.info(f"{message.from_user.username}: {message.text}")
    await message.answer(message.text)


async def main():
    """Главная функция"""
    logger.info("Бот запущен!")
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Ошибка: {e}")


if __name__ == "__main__":
    asyncio.run(main())