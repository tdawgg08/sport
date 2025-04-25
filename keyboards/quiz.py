from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

def question_1(answered) -> InlineKeyboardMarkup:
    if not answered:
        keyboard = [
            [InlineKeyboardButton(text="Здоровье", callback_data="quiz-1-1")],
            [InlineKeyboardButton(text="Похудение", callback_data="quiz-1-2")],
            [InlineKeyboardButton(text="Спортивные результаты", callback_data="quiz-1-3")],
            ]
    match answered:
        case 1:
            keyboard = [
                [InlineKeyboardButton(text="✅Здоровье", callback_data="pass")],
                [InlineKeyboardButton(text="Похудение", callback_data="pass")],
                [InlineKeyboardButton(text="Спортивные результаты", callback_data="pass")],
                ]
        case 2:
            keyboard = [
                [InlineKeyboardButton(text="Здоровье", callback_data="pass")],
                [InlineKeyboardButton(text="✅Похудение", callback_data="pass")],
                [InlineKeyboardButton(text="Спортивные результаты", callback_data="pass")],
                ]
        case 3:
            keyboard = [
                [InlineKeyboardButton(text="Здоровье", callback_data="pass")],
                [InlineKeyboardButton(text="Похудение", callback_data="pass")],
                [InlineKeyboardButton(text="✅Спортивные результаты", callback_data="pass")],
                ]
    keyboard.append(
        [
           InlineKeyboardButton(text = '⬅️', callback_data='pass'),
           InlineKeyboardButton(text = '[ 1 ]', callback_data='pass'),
           InlineKeyboardButton(text = '➡️', callback_data='quiz-2'),
        ]
    )        
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def question_2(answered) -> InlineKeyboardMarkup:
    if not answered:
        keyboard = [
            [InlineKeyboardButton(text="Фитнес", callback_data="quiz-2-1")],
            [InlineKeyboardButton(text="Бег", callback_data="quiz-2-2")],
            [InlineKeyboardButton(text="Плавание", callback_data="quiz-2-3")],
            ]
    match answered:
        case 1:
            keyboard = [
                [InlineKeyboardButton(text="✅Фитнес", callback_data="pass")],
                [InlineKeyboardButton(text="Бег", callback_data="pass")],
                [InlineKeyboardButton(text="Плавание", callback_data="pass")],
                ]
        case 2:
            keyboard = [
                [InlineKeyboardButton(text="Фитнес", callback_data="pass")],
                [InlineKeyboardButton(text="✅Бег", callback_data="pass")],
                [InlineKeyboardButton(text="Плавание", callback_data="pass")],
                ]
        case 3:
            keyboard = [
                [InlineKeyboardButton(text="Фитнес", callback_data="pass")],
                [InlineKeyboardButton(text="Бег", callback_data="pass")],
                [InlineKeyboardButton(text="✅Плавание", callback_data="pass")],
                ]
    keyboard.append(
        [
           InlineKeyboardButton(text = '⬅️', callback_data='quiz-1'),
           InlineKeyboardButton(text = '[ 2 ]', callback_data='pass'),
           InlineKeyboardButton(text = '➡️', callback_data='quiz-3'),
        ]
    )        
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def question_3(answered) -> InlineKeyboardMarkup:
    if not answered:
        keyboard = [
            [InlineKeyboardButton(text="Похудение", callback_data="quiz-3-1")],
            [InlineKeyboardButton(text="Набор массы", callback_data="quiz-3-2")],
            [InlineKeyboardButton(text="Здоровье", callback_data="quiz-3-3")],
            ]
    match answered:
        case 1:
            keyboard = [
                [InlineKeyboardButton(text="✅Похудение", callback_data="pass")],
                [InlineKeyboardButton(text="Набор массы", callback_data="pass")],
                [InlineKeyboardButton(text="Здоровье", callback_data="pass")],
                ]
        case 2:
            keyboard = [
                [InlineKeyboardButton(text="Похудение", callback_data="pass")],
                [InlineKeyboardButton(text="✅Набор массы", callback_data="pass")],
                [InlineKeyboardButton(text="Здоровье", callback_data="pass")],
                ]
        case 3:
            keyboard = [
                [InlineKeyboardButton(text="Похудение", callback_data="pass")],
                [InlineKeyboardButton(text="Набор массы", callback_data="pass")],
                [InlineKeyboardButton(text="✅Здоровье", callback_data="pass")],
                ]
    keyboard.append(
        [
           InlineKeyboardButton(text = '⬅️', callback_data='quiz-2'),
           InlineKeyboardButton(text = '[ 3 ]', callback_data='pass'),
           InlineKeyboardButton(text = '➡️', callback_data='quiz-4'),
        ]
    )        
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def question_4(answered) -> InlineKeyboardMarkup:
    if not answered:
        keyboard = [
            [InlineKeyboardButton(text="1-3 часа", callback_data="quiz-4-1")],
            [InlineKeyboardButton(text="3-5 часов", callback_data="quiz-4-2")],
            [InlineKeyboardButton(text="7+ часов", callback_data="quiz-4-3")],
            ]
    match answered:
        case 1:
            keyboard = [
                [InlineKeyboardButton(text="✅1-3 часа", callback_data="pass")],
                [InlineKeyboardButton(text="3-7 часов", callback_data="pass")],
                [InlineKeyboardButton(text="7+ часов", callback_data="pass")],
                ]
        case 2:
            keyboard = [
                [InlineKeyboardButton(text="1-3 часа", callback_data="pass")],
                [InlineKeyboardButton(text="✅3-7 часов", callback_data="pass")],
                [InlineKeyboardButton(text="7+ часов", callback_data="pass")],
                ]
        case 3:
            keyboard = [
                [InlineKeyboardButton(text="1-3 часа", callback_data="pass")],
                [InlineKeyboardButton(text="3-7 часов", callback_data="pass")],
                [InlineKeyboardButton(text="✅7+ часов", callback_data="pass")],
                ]
    keyboard.append(
        [
           InlineKeyboardButton(text = '⬅️', callback_data='quiz-3'),
           InlineKeyboardButton(text = '[ 4 ]', callback_data='pass'),
           InlineKeyboardButton(text = '➡️', callback_data='quiz-5'),
        ]
    )        
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def question_5(answered) -> InlineKeyboardMarkup:
    if not answered:
        keyboard = [
            [InlineKeyboardButton(text="Сам", callback_data="quiz-5-1")],
            [InlineKeyboardButton(text="С тренером", callback_data="quiz-5-2")],
            [InlineKeyboardButton(text="Групповые занятия", callback_data="quiz-5-3")],
            ]
    match answered:
        case 1:
            keyboard = [
                [InlineKeyboardButton(text="✅Сам", callback_data="pass")],
                [InlineKeyboardButton(text="С тренером", callback_data="pass")],
                [InlineKeyboardButton(text="Групповые занятия", callback_data="pass")],
                ]
        case 2:
            keyboard = [
                [InlineKeyboardButton(text="Сам", callback_data="pass")],
                [InlineKeyboardButton(text="✅С тренером", callback_data="pass")],
                [InlineKeyboardButton(text="Групповые занятия", callback_data="pass")],
                ]
        case 3:
            keyboard = [
                [InlineKeyboardButton(text="Сам", callback_data="pass")],
                [InlineKeyboardButton(text="С тренером", callback_data="pass")],
                [InlineKeyboardButton(text="✅Групповые занятия", callback_data="pass")],
                ]
    keyboard.append(
        [
           InlineKeyboardButton(text = '⬅️', callback_data='quiz-4'),
           InlineKeyboardButton(text = '[ 5 ]', callback_data='pass'),
           InlineKeyboardButton(text = '➡️', callback_data='quiz-6'),
        ]
    )        
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def question_6(answered) -> InlineKeyboardMarkup:
    if not answered:
        keyboard = [
            [InlineKeyboardButton(text="Да, важно", callback_data="quiz-6-1")],
            [InlineKeyboardButton(text="Нет, не важно", callback_data="quiz-6-2")],
            [InlineKeyboardButton(text="Уже есть", callback_data="quiz-6-3")],
            ]
    match answered:
        case 1:
            keyboard = [
                [InlineKeyboardButton(text="✅Да, важно", callback_data="pass")],
                [InlineKeyboardButton(text="Нет, не важно", callback_data="pass")],
                [InlineKeyboardButton(text="Уже есть", callback_data="pass")],
                ]
        case 2:
            keyboard = [
                [InlineKeyboardButton(text="Да, важно", callback_data="pass")],
                [InlineKeyboardButton(text="✅Нет, не важно", callback_data="pass")],
                [InlineKeyboardButton(text="Уже есть", callback_data="pass")],
                ]
        case 3:
            keyboard = [
                [InlineKeyboardButton(text="Да, важно", callback_data="pass")],
                [InlineKeyboardButton(text="Нет, не важно", callback_data="pass")],
                [InlineKeyboardButton(text="✅Уже есть", callback_data="pass")],
                ]
    keyboard.append(
        [
           InlineKeyboardButton(text = '⬅️', callback_data='quiz-5'),
           InlineKeyboardButton(text = '[ 6 ]', callback_data='pass'),
           InlineKeyboardButton(text = 'Меню', callback_data='quiz-7'),
        ]
    )        
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def question_7(answered) -> InlineKeyboardMarkup:
    if not answered:
        keyboard = [
            [InlineKeyboardButton(text="До 18", callback_data="quiz-7-1")],
            [InlineKeyboardButton(text="18-25", callback_data="quiz-7-2")],
            [InlineKeyboardButton(text="25+", callback_data="quiz-7-3")],
            ]
    match answered:
        case 1:
            keyboard = [
                [InlineKeyboardButton(text="✅До 18", callback_data="pass")],
                [InlineKeyboardButton(text="18-25", callback_data="pass")],
                [InlineKeyboardButton(text="25+", callback_data="pass")],
                ]
        case 2:
            keyboard = [
                [InlineKeyboardButton(text="До 18", callback_data="pass")],
                [InlineKeyboardButton(text="✅18-25", callback_data="pass")],
                [InlineKeyboardButton(text="25+", callback_data="pass")],
                ]
        case 3:
            keyboard = [
                [InlineKeyboardButton(text="До 18", callback_data="pass")],
                [InlineKeyboardButton(text="18-25", callback_data="pass")],
                [InlineKeyboardButton(text="✅25+", callback_data="pass")],
                ]
    keyboard.append(
        [
           InlineKeyboardButton(text = '⬅️', callback_data='quiz-6'),
           InlineKeyboardButton(text = '[ 7 ]', callback_data='pass'),
           InlineKeyboardButton(text = 'Меню', callback_data='menu'),
        ]
    )        
    return InlineKeyboardMarkup(inline_keyboard=keyboard)