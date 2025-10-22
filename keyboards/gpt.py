from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def gpt_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Анализ статистики", callback_data="deepseek_analize")],
            [InlineKeyboardButton(text='Задать вопрос', callback_data='deepseek')]
            
        ]
    )