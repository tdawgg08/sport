from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


def pagination_keyboard(products_list, current_page, type_callback: int):
    items_per_page = 10
    start_index = (current_page - 1) * items_per_page
    end_index = start_index + items_per_page
    items_page = products_list[start_index:end_index]
    result_list_buttons = []

    if type_callback == 1:
        # products for current page in handler add_meal
        for item in items_page:
            result_list_buttons.append([InlineKeyboardButton(text=item, callback_data=f'first_type:{products_list.index(item)}')])
    elif type_callback == 2:
        # meals for current page in handler delete_meal
        for item in items_page:
            result_list_buttons.append([InlineKeyboardButton(text=item, callback_data=f'second_type:{str(item)}')])
        result_list_buttons = list(reversed(result_list_buttons))
    elif type_callback == 3:
        # products for current page in handler delete_product
        for item in items_page:
            result_list_buttons.append([InlineKeyboardButton(text=item, callback_data=f'third_type:{str(item)}')])
        result_list_buttons = list(reversed(result_list_buttons))

    func_buttons_row = []

    if current_page > 1:
        func_buttons_row.append(InlineKeyboardButton(text='<', callback_data=f"page:prev_page:{current_page}"))
    else:
        func_buttons_row.append(InlineKeyboardButton(text='-', callback_data="pass"))

    text = f'{current_page}/{(len(products_list) + items_per_page - 1) // items_per_page}'
    func_buttons_row.append(
        InlineKeyboardButton(text=text, callback_data="pass"))

    if end_index < len(products_list):
        func_buttons_row.append(InlineKeyboardButton(text='>', callback_data=f"page:next_page:{current_page}"))
    else:
        func_buttons_row.append(InlineKeyboardButton(text='-', callback_data="pass"))

    result_list_buttons.append(func_buttons_row)
    products_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=result_list_buttons)
    return products_inline_keyboard


def end_keyboard() -> InlineKeyboardMarkup:
    result_list_buttons = []

    result_list_buttons.append([InlineKeyboardButton(text='Добавить продукт', callback_data="add_product")])
    result_list_buttons.append([InlineKeyboardButton(text='Удалить продукт', callback_data="delete_product")])
    result_list_buttons.append([InlineKeyboardButton(text='Отменить добавление приёма', callback_data="cancel_meal")])
    result_list_buttons.append([InlineKeyboardButton(text='Подтвердить добавление приёма', callback_data="insert_meal")])

    end_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=result_list_buttons)
    return end_inline_keyboard


def keyboard_end():
    result_list_buttons = []

    result_list_buttons.append([KeyboardButton(text='конец')])

    button_end = ReplyKeyboardMarkup(keyboard=result_list_buttons, resize_keyboard=True)
    return button_end



def add_product_keyboard() -> InlineKeyboardMarkup:
    result_list_buttons = []

    result_list_buttons.append([InlineKeyboardButton(text='Отменить добавление продукта', callback_data="cancel_product")])
    result_list_buttons.append([InlineKeyboardButton(text='Подтвердить добавление продукта', callback_data="insert_product")])

    add_product_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=result_list_buttons)
    return add_product_inline_keyboard


def calendar_keyboard():
    result_list_buttons = []

    result_list_buttons.append([InlineKeyboardButton(text='Неделя', callback_data="week")])
    result_list_buttons.append([InlineKeyboardButton(text='День', callback_data="day")])

    calendar_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=result_list_buttons)
    return calendar_inline_keyboard


def start_reply_keyboard():
    result_list_buttons = []

    result_list_buttons.append([KeyboardButton(text='Добавить приём пищи'), KeyboardButton(text='Добавить продукт')])
    result_list_buttons.append([KeyboardButton(text='Удалить приём пищи'), KeyboardButton(text='Удалить продукт')])
    result_list_buttons.append([KeyboardButton(text='Календарь')])

    start_reply_keyboard = ReplyKeyboardMarkup(keyboard=result_list_buttons, resize_keyboard=True)
    return start_reply_keyboard