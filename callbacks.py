from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.exceptions import TelegramBadRequest
from aiogram import Router, F, types
from aiogram.filters import Command

from typing import Optional
from contextlib import suppress

num_router = Router()

user_data = {}
class NumbersCallbackFactory(CallbackData, prefix = 'fabnum'):
    action: str 
    value: Optional[int] = None

def get_keyboard():
    builder = InlineKeyboardBuilder

    builder.button(
        InlineKeyboardButton(text = '-2', callback_data=NumbersCallbackFactory(action='change', value = '-2')).pack()
    )  
    builder.button(
        InlineKeyboardButton(text = '-1', callback_data=NumbersCallbackFactory(action='change', value = '-1')).pack()
    )
    builder.button(
        InlineKeyboardButton(text = '+2', callback_data=NumbersCallbackFactory(action='change', value = '+2')).pack()
    )
    builder.button(
        InlineKeyboardButton(text = '-`', callback_data=NumbersCallbackFactory(action='change', value = '-`')).pack()
    )
    builder.button(
        InlineKeyboardButton(text = 'Подтвердить', callback_data=NumbersCallbackFactory(action='finish')).pack()
    )

    builder.adjust(4)
    return builder.as_markup()

async def update_num(message: types.Message, new_value: int):
    with suppress(TelegramBadRequest):
        await message.edit_text(
            f'Укажите число: {new_value}',
            reply_markup=get_keyboard()
        )

@num_router.message(Command('numbers'))
async def num_numbers(message: types.Message):
    user_data[message.from_user.id] = 0
    await message.answer(
        'Укажите число: 0',
        reply_markup=get_keyboard()
    )
@num_router.callback_query(NumbersCallbackFactory.filter())    
async def callback_num(
    callback : types.callback_query,
    callback_data : NumbersCallbackFactory
    ):
    user_value = user_data[callback.from_user.id, 0]
    if callback_data.action == 'change':
        user_data[callback.from_user.id] == user_value + callback_data.value
        await update_num(callback.message, user_data + callback_data.value)
    else:
        await callback.answer(f'Ваше число: {user_value}')    



