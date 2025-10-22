from aiogram.types import CallbackQuery
from aiogram import Router, F
from database.models import Food
from misc.scheduler_update_date import update_time
from keyboards.list_of_calories import keyboard_to_list_of_calories
router = Router()

@router.callback_query(F.data == 'calories')
async def output_daily_calories(callback : CallbackQuery):
    information = await Food.filter(telegram_id = callback.from_user.id, date = update_time())
    if information:
        string = ''
        total_protein = []
        total_fats = []
        total_carbs = []
        total_kcal = []
        product_list = []
        quantity = []
        for food in information:
            product_list.append(food.name)
            total_carbs.append(food.carbs)
            total_protein.append(food.protein)
            total_kcal.append(food.kcal)
            total_fats.append(food.fats)
            quantity.append(food.quantity)
        for i in range(len(product_list)):
            string += f'Блюдо: {product_list[i]}. Белков {total_protein[i]}гр. Жиров {total_fats[i]}гр. Углеводов {total_carbs}гр. Вес {quantity[i]}гр. Калорий {total_kcal[i]}. \n'

        await callback.message.answer(string + f'Всего белков {sum(total_protein)}. Всего жиров {sum(total_fats)}. Всего углеводов {sum(total_carbs)}. Всего калорий {sum(total_kcal)}.', reply_markup=keyboard_to_list_of_calories())
        await callback.answer()
    else:
        await callback.message.answer('Список продуктов пуст', reply_markup=keyboard_to_list_of_calories())
        await callback.answer()    