from statistics import quantiles
from aiogram import Router, F
from aiogram.types import Message
from aiogram.types import CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from database.models import Food, Products
from keyboards.list_of_calories import keyboard_to_list_of_calories
from misc.scheduler_update_date import update_time

router = Router()

class FoodQuantity(StatesGroup):
    waiting_quantity = State()


@router.callback_query(F.data.startswith('product_'))
async def product_append(callback : CallbackQuery, state : FSMContext):
    datas = int(callback.data.replace('product_', ''))
    await callback.message.answer(
        'Пожалуйста, введите сколько вы грамм продукта съели'
    )
    await state.set_data({'product_id' : datas})

    await state.set_state(FoodQuantity.waiting_quantity)
    await callback.answer()
    

@router.message(FoodQuantity.waiting_quantity)
async def food_quantity(message : Message, state : FSMContext): 
    try:
        weight = float(message.text)
        if weight <= 0:
            message.answer('Вес должен быть больше нуля грамм!')
            return 
        data = await state.get_data()
        
        product_id = data['product_id']
        product = await Products.get(id = product_id)
        
        await Food.create(
        telegram_id = message.from_user.id,
        username = message.from_user.username,
        date = update_time(),
        name = product.name,
        protein = product.protein * weight / 100,
        fats = product.fats * weight / 100,
        carbs = product.carbs * weight / 100,
        kcal = product.kcal * weight / 100,
        quantity = weight
    )

        await message.answer("Изменение добавлено!", reply_markup=keyboard_to_list_of_calories())   
        
    except ValueError:
        await message.answer('Введите вещественное число!')
    finally:
        await state.clear()