from aiogram import Router, F
from aiogram.types import Message 
from aiogram.filters import Command
from keyboards.start import start_keyboard
from aiogram.fsm.context import FSMContext



router = Router()

@router.message(Command('start'))
async def start_command(message: Message):
    await message.answer(
        f"Привет, {message.from_user.first_name}!\n"
        "Ты попал в бота \"Интеллектуальный помощник по спортивному планированию\"\n"
        "Нажми кнопку ниже, чтобы начать тест 👇",
        reply_markup=start_keyboard()
    )

