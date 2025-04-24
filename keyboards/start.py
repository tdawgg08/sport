from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def start_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Начать")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )