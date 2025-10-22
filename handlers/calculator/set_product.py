from tortoise.expressions import Q
from aiogram.types import CallbackQuery, Message
from aiogram import Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.models import Products

class SetProduct(StatesGroup):
    waiting_product_name = State()

router = Router()

@router.callback_query(F.data == 'append_calories')
async def set_products(callback : CallbackQuery, state : FSMContext):
    await callback.message.answer('Введите продукт, который хотите добавить')
    await state.set_state(SetProduct.waiting_product_name)
    await callback.answer()

@router.message(SetProduct.waiting_product_name)
async def show_products_keyboard(message: Message, state: FSMContext):
    search_name = message.text.strip().lower()
    products = await Products.filter(Q(name__icontains=search_name))
    if products:
        buttons = []
        for product in products:
            buttons.append([
                InlineKeyboardButton(
                    text=f"{product.name} - {product.kcal} ккал",
                    callback_data=f"product_{product.id}"
                )
            ])
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        
        await message.answer("Выберите продукт:", reply_markup=keyboard)
    else:
        await message.answer("Продукты не найдены")
    
    await state.clear()