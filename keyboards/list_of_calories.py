from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def keyboard_to_list_of_calories():
    keyboard = [
        [InlineKeyboardButton(text='Меню', callback_data='back')],
        [InlineKeyboardButton(text='Добавить калории', callback_data='append_calories')],
        [InlineKeyboardButton(text='Мои калории', callback_data='calories')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
