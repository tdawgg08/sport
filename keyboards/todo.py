from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_todolist_inline_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="Add Task", callback_data="add_task")
    keyboard_builder.button(text="Delete Task", callback_data="delete_task")
    keyboard_builder.button(text="List All Tasks", callback_data="todo")
    keyboard_builder.button(text="Menu", callback_data="back")

    keyboard_builder.adjust(1)

    return keyboard_builder.as_markup()