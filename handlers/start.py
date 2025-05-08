from aiogram import Router, F
from aiogram.types import Message 
from aiogram.filters import Command
from keyboards.start import start_keyboard
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonPollType
from aiogram.utils.keyboard import ReplyKeyboardBuilder


router = Router()

# @router.message(Command('start'))
# async def start_command(message: Message):
#     await message.answer(
#         f"Привет, {message.from_user.first_name}!\n"
#         "Ты попал в бота \"Интеллектуальный помощник по спортивному планированию\"\n"
#         "Нажми кнопку ниже, чтобы начать тест 👇",
#         reply_markup=start_keyboard()
#     )
@router.message(Command('start'))
async def start_command(message : Message):
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text = 'Запросить геолокацию', request_location=True),
        KeyboardButton(text = 'Запросить контакт', request_contact= True)
    )
    builder.row(KeyboardButton(
        text="Создать викторину",
        request_poll=KeyboardButtonPollType(type="quiz")))
    await message.answer('Выберете действие:', reply_markup=builder.as_markup(resize_keyboard=True))
    await message.delete()
    