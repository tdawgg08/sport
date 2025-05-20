from datetime import datetime, timedelta
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import callback_query
from sqlalchemy import select, and_, extract
from database.database import AsyncSessionLocal
from database.requests import consumption, delete_meal_from_db, delete_product_from_db
from database.models import Consumption, Products
from handlers.calculator.dynamic import Meal
from keyboards.calculator.keyboards import pagination_keyboard, start_reply_keyboard

router = Router()

@router.callback_query(F.data.startswith("pass"))
async def pass_func(call: callback_query):
    await call.answer()


@router.callback_query(F.data.startswith("page"))
async def handle_pagination_buttons(call: callback_query, state: FSMContext):
    data = call.data.split(':')
    action = data[1]
    current_page = int(data[2])

    if action == 'prev_page':
        current_page -= 1
    elif action == 'next_page':
        current_page += 1

    message = call.message

    data = await state.get_data()
    list_products = data['list_products']

    markup = pagination_keyboard(list_products, current_page, type_callback=1)
    await message.edit_text(
        text=message.text,
        reply_markup=markup
    )

    await call.answer()

########################################################################################################################
# Three types callbacks for pagination_keyboard

# type == 1
@router.callback_query(F.data.startswith('first_type'))
async def callback_product(call: callback_query, state: FSMContext):
    await call.message.delete()

    index_product = int(call.data.split(':')[1])
    data = await state.get_data()
    list_products = data['list_products']
    product = list_products[index_product]
    await call.message.answer(f'Вы выбрали продукт - {product}. Теперь укажите вес съеденного продукта (в граммах).')
    await state.update_data(name_product=product)
    await state.set_state(Meal.WEIGHT_PRODUCT)
    await call.answer()
    return product

# type == 2
@router.callback_query(F.data.startswith('second_type'))
async def callback_product(call: callback_query, state: FSMContext):
    data = await state.get_data()

    name_meal = call.data.split(':')[1]
    user_id = data['user_id_for_delete_meal']

    await delete_meal_from_db(user_id=user_id, meal_name=name_meal)
    await call.message.delete()
    await call.message.answer(f'Приём пищи - {name_meal}, удалён.')
    await state.clear()

# type == 3
@router.callback_query(F.data.startswith('third_type'))
async def callback_product(call: callback_query, state: FSMContext):
    data = await state.get_data()

    name_product = call.data.split(':')[1]
    user_id = data['user_id_for_delete']

    await delete_product_from_db(user_id=user_id, product_name=name_product)
    await call.message.delete()
    await call.message.answer(f'Продукт - {name_product}, удалён.')
    await state.clear()
########################################################################################################################


@router.callback_query(F.data.startswith('add_product'))
async def callback_add_product(call: callback_query, state: FSMContext):
    await call.message.answer('Введите продукты. Отправьте "конец", когда закончите.')
    await state.set_state(Meal.DATA_PRODUCTS)
    await call.answer()


@router.callback_query(F.data.startswith('delete_product'))
async def callback_delete_product(call: callback_query, state: FSMContext):
    await call.message.answer('Введите порядковый номер продукта из списка для его удаления.')
    await state.set_state(Meal.GET_INDEX_PRODUCT)
    await call.answer()


@router.callback_query(F.data.startswith('cancel_meal'))
async def callback_cancel_meal(call: callback_query, state: FSMContext):
    markup = start_reply_keyboard()
    await state.clear()
    await call.message.answer('Приём пищи удалён.', reply_markup=markup)
    await call.answer()


@router.callback_query(F.data.startswith('insert_meal'))
async def callback_insert_meal(call: callback_query, state: FSMContext):
    markup = start_reply_keyboard()
    data = await state.get_data()
    user_id = call.from_user.id
    meal_name = data['name']
    list_text = []
    count = 1
    weight = 0
    calories_result = 0
    proteins_result = 0
    fats_result = 0
    carbohydrates_result = 0

    for product in data['list_user_products']:
        list_text.append(f"{count}) {product['name_product']}")
        weight += product['weight_product']
        calories_result += product['calories']
        proteins_result += product['proteins']
        fats_result += product['fats']
        carbohydrates_result += product['carbohydrates']
        count += 1

    if len(data['list_user_products']) > 0:
        async with AsyncSessionLocal() as db:
            consumption = Consumption(
                user_id=user_id,
                meal_name=meal_name,
                product_list=' | '.join(list_text),
                weight=weight,
                calories_result=calories_result,
                proteins_result=proteins_result,
                fats_result=fats_result,
                carbohydrates_result=carbohydrates_result
            )

            db.add(consumption)
            await db.commit()
        await call.message.delete()
        await call.message.answer('Приём пищи добавлен.', reply_markup=markup)
        await state.clear()
    else:
        await call.message.answer('Список продуктов пуст.')
        await call.answer()






@router.callback_query(F.data.startswith('cancel_product'))
async def callback_cancel_product(call: callback_query, state: FSMContext):
    await state.clear()
    await call.message.answer('Продукт удалён.')
    await call.answer()


@router.callback_query(F.data.startswith('insert_product'))
async def callback_insert_product(call: callback_query, state: FSMContext):
    data = await state.get_data()
    user_id = call.from_user.id

    name_product = data["product_add_name"]
    calories = data['calories']
    proteins = data['proteins']
    fats = data['proteins']
    carbohydrates = data['carbohydrates']

    async with AsyncSessionLocal() as db:
        products = Products(
            user_id=user_id,
            product_name=name_product,
            calories=calories,
            proteins=proteins,
            fats=fats,
            carbohydrates=carbohydrates
        )

        db.add(products)
        await db.commit()

    await state.clear()
    await call.message.answer('Продукт добавлен.')
    await call.answer()









@router.callback_query(F.data.startswith('day'))
async def callback_calendar_day(call: callback_query, state: FSMContext):
    now = datetime.now()
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = now.replace(hour=23, minute=59, second=59, microsecond=999999)

    data = await state.get_data()
    user_id = data['user_id_for_calendar']

    query = select(consumption).where(
        and_(
            consumption.c.user_id == user_id,
            consumption.c.day >= start_of_day,
            consumption.c.day <= end_of_day
        )
    )

    async with AsyncSessionLocal() as db_session:
        await call.message.delete()


        result = await db_session.execute(query)
        rows = result.fetchall()

        result_text = ""
        result_calories = 0
        result_proteins = 0
        result_fats = 0
        result_carbohydrates = 0

        for item in rows:
            index, user_id, date, meal_name, product_text, weight, calories, proteins, fats, carbohydrates = item
            result_calories += calories
            result_proteins += proteins
            result_fats += fats
            result_carbohydrates += carbohydrates

            products = [product.strip() for product in product_text.split(' | ')]

            hours = date.hour
            minutes = date.minute

            result_text += f"{str(meal_name).capitalize()} ({hours:02d}:{minutes:02d}):\n"
            for product in products:
                result_text += f"{product}\n"
            result_text += f"К: {calories} Б: {proteins} Ж: {fats} У: {carbohydrates}\n\n"

        result_text += (f'Итог за день:\n'
                        f'К: {result_calories} Б: {result_proteins} Ж: {result_fats} У: {result_carbohydrates}')

        await call.message.answer(result_text)
        await state.clear()
        await call.answer()



@router.callback_query(F.data.startswith('week'))
async def callback_calendar_week(call: callback_query, state: FSMContext):
    await call.message.delete()


    now = datetime.now()
    start_of_week = now - timedelta(days=now.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    data = await state.get_data()
    user_id = data['user_id_for_calendar']

    query = select(consumption).where(
        and_(
            consumption.c.user_id == user_id,
            extract('week', consumption.c.day) == extract('week', start_of_week),
            extract('year', consumption.c.day) == extract('year', start_of_week)
        )
    )

    async with AsyncSessionLocal() as db_session:
        result = await db_session.execute(query)
        consumption_data = result.fetchall()

    week_data = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: []}

    def extract_data(item):
        id, user_id, date, meal_name, product_text, weight, calories, proteins, fats, carbohydrates = item
        return {
            'id': id,
            'user_id': user_id,
            'date': date,
            'meal_name': meal_name,
            'product_text': product_text,
            'weight': weight,
            'calories': calories,
            'proteins': proteins,
            'fats': fats,
            'carbohydrates': carbohydrates,
        }

    for item in consumption_data:
        data = extract_data(item)
        date = data['date']
        day_of_week = date.weekday()
        week_data[day_of_week].append(data)

    report = ""
    total_week_calories = 0
    total_week_proteins = 0
    total_week_fats = 0
    total_week_carbohydrates = 0

    for day in range(7):
        day_name = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье'][day]

        day_report = f"{day_name}:\n"
        if week_data[day]:
            day_calories = 0
            day_proteins = 0
            day_fats = 0
            day_carbohydrates = 0
            day_product_count = 0
            list_meals = []

            for item in week_data[day]:
                meal_name = item['meal_name']
                products = item['product_text'].split(' | ')
                list_meals.append(str(meal_name).capitalize())
                for product in products:
                    day_product_count += 1
                day_calories += item['calories']
                day_proteins += item['proteins']
                day_fats += item['fats']
                day_carbohydrates += item['carbohydrates']

            day_report += f"Список приёмов: {', '.join(list_meals)}\n"
            day_report += f"Кол-во продуктов: {day_product_count}\n"
            day_report += f"Итог за день:\n"
            day_report += f"К: {day_calories} Б: {day_proteins} Ж: {day_fats} У: {day_carbohydrates}\n\n"

            total_week_calories += day_calories
            total_week_proteins += day_proteins
            total_week_fats += day_fats
            total_week_carbohydrates += day_carbohydrates
        else:
            day_report += "Нет приёмов пищи в этот день\n\n"

        report += day_report

    report += f"Итог за неделю:\n"
    report += f"К: {total_week_calories} Б: {total_week_proteins} Ж: {total_week_fats} У: {total_week_carbohydrates}"

    await call.message.answer(report)
    await state.clear()
    await call.answer()