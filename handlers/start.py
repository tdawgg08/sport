from aiogram import Router
from aiogram.types import Message 
from aiogram.filters import Command
from keyboards.start import start_keyboard
from keyboards.menu import menu_kb

from database.models import User

router = Router()

@router.message(Command('start'))
async def start_command(message: Message):
    people = await User.filter(telegram_id = message.from_user.id).first()
    if not people:
        await message.answer(
            f"Привет, {message.from_user.first_name}!\n"
            "Ты попал в бота \"Интеллектуальный помощник по спортивному планированию\"\n"
            "Нажми кнопку ниже, чтобы начать тест 👇",
            reply_markup=start_keyboard()
        ) 
    else:
        if people.first_answer is None or people.second_answer is None or people.third_answer is None or people.fourth_answer is None or people.fifth_answer is None or people.sixth_answer is None or people.seventh_answer is None: 
            await message.answer('Пожалуйста, пройдите тест', reply_markup=start_keyboard())
        else:
            await message.answer('Меню', reply_markup=menu_kb())    
    