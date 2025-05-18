from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def gpt_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="back")],
            
        ]
    )