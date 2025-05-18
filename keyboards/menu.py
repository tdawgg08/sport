from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def menu_kb() -> InlineKeyboardMarkup:
    
    keyboard = [
        [InlineKeyboardButton(text="📝 Todo List", callback_data="todo"),
         InlineKeyboardButton(text="Задать вопрос", callback_data="question"),
         InlineKeyboardButton(text="Калькулятор калорий", callback_data="calculator"),]
    ]
                
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)