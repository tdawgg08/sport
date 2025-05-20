from aiogram import Router, F
from aiogram.types import Message 
from aiogram.filters import Command
from keyboards.start import start_keyboard
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonPollType
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from database.database import AsyncSessionLocal
from database.models import Users



router = Router()

@router.message(Command('start'))
async def start_command(message: Message):
    username = message.from_user.username
    user_id = message.from_user.id
    
    try:
        async with AsyncSessionLocal() as db:
            user = Users(
                user_id=user_id
            )

            db.add(user)
            await db.commit()
            await message.answer(
        f"Привет, {message.from_user.first_name}!\n"
        "Ты попал в бота \"Интеллектуальный помощник по спортивному планированию\"\n"
        "Нажми кнопку ниже, чтобы начать тест 👇",
        reply_markup=start_keyboard()
    )
    
    except:
        pass
    
    