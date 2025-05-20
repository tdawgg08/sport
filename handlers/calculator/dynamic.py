from math import ceil
from re import sub
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from database.requests import products_from_db, convert_weight_product, meals_from_db, products_user_from_db
from handlers.calculator.universal_funcs import text_meal
from keyboards.calculator.keyboards import end_keyboard, add_product_keyboard, calendar_keyboard, pagination_keyboard, \
    keyboard_end

router = Router()

########################################################################################################################
# AddMeal
class Meal(StatesGroup):
    GET_NAME_MEAL = State()
    DATA_PRODUCTS = State()
    NAME_PRODUCT = State()
    WEIGHT_PRODUCT = State()
    END_MEAL = State()
    GET_INDEX_PRODUCT = State()



@router.message(F.text == 'Добавить приём пищи')
async def add_meal(message: Message, state: FSMContext):
    await message.answer('Введите название приёма пищи.')
    await state.update_data(list_user_products=list())
    await state.set_state(Meal.GET_NAME_MEAL)

@router.message(Meal.GET_NAME_MEAL)
async def get_name_meal(message: Message, state: FSMContext):
    name = sub(r'[/]', '', message.text)
    await message.answer(f'Название приёма пищи - {name}. Теперь введите продукты. Отправьте "конец", когда закончите.')
    await state.update_data(name=name)
    await state.set_state(Meal.DATA_PRODUCTS)


@router.message(Meal.DATA_PRODUCTS)
async def get_product(message: Message, state: FSMContext):
    word = message.text
    list_products = await products_from_db(word, user_id=message.from_user.id)
    if list_products:
        markup = pagination_keyboard(list_products, current_page=1, type_callback=1)
        await message.answer('Выберите продукт:', reply_markup=markup)
        await state.update_data(list_products=list_products)
    elif word.lower() == 'конец':
        try:
            data = await state.get_data()
            check_except = data['list_user_products'][0]

            await state.set_state(Meal.END_MEAL)
            name_meal = data['name']
            list_user_products = data['list_user_products']

            markup = end_keyboard()
            await message.answer(text_meal(name=name_meal, list_user_products=list_user_products), reply_markup=markup)
        except:
            await message.answer('Вы не выбрали ни один продукт.')
    else:
        await message.answer('Продукт не найден.')


@router.message(Meal.WEIGHT_PRODUCT)
async def get_weight_product(message: Message, state: FSMContext):
    try:
        weight = float(sub(r'[,]', '.', message.text))
        await state.update_data(weight_product=weight)
        data = await state.get_data()
        name_product = data['name_product']
        weight_product = float(data['weight_product'])

        dictionary_result_product = await convert_weight_product(name_product=name_product, weight=weight)

        markup = keyboard_end()

        await message.answer(f'Продукт: {dictionary_result_product["product_name"]}\n'
                             f'Вес: {ceil(weight_product)} гр.\n'
                             f'Калории: {dictionary_result_product["calories"]}\n'
                             f'Белки: {dictionary_result_product["proteins"]}\n'
                             f'Жиры: {dictionary_result_product["fats"]}\n'
                             f'Углеводы: {dictionary_result_product["carbohydrates"]}', reply_markup=markup)

        list_user_products = data.get('list_user_products', [])
        list_user_products.append({'name_product': name_product,
                                   'weight_product': int(weight_product),
                                   'calories': dictionary_result_product["calories"],
                                   'proteins': dictionary_result_product["proteins"],
                                   'fats': dictionary_result_product["fats"],
                                   'carbohydrates': dictionary_result_product['carbohydrates']})

        await state.update_data(list_user_products=list_user_products)
        await state.set_state(Meal.DATA_PRODUCTS)
    except:
        await message.answer('Введите корректный вес.')


@router.message(Meal.GET_INDEX_PRODUCT)
async def get_index_product(message: Message, state: FSMContext):
    try:
        index_product = int(message.text)
        await state.update_data(index=index_product)
        data = await state.get_data()
        list_user_products = data['list_user_products']
        try:
            del list_user_products[index_product - 1]
            await state.update_data(list_user_products=list_user_products)

            name_meal = data['name']
            list_user_products = data['list_user_products']

            markup = end_keyboard()
            await message.answer(text_meal(name=name_meal, list_user_products=list_user_products), reply_markup=markup)

            await state.set_state(Meal.END_MEAL)
        except:
            await message.answer("Введён некорректный номер.")
    except:
        await message.answer('Введите порядковый номер продукта.')
########################################################################################################################
# DeleteMeal
class DeleteMeal(StatesGroup):
    USER_ID_FOR_DELETE = State()


@router.message(F.text == 'Удалить приём пищи')
async def delete_meal(message: Message, state: FSMContext):
    user_id_for_delete_meal = message.from_user.id

    list_products = await meals_from_db(user_id=message.from_user.id)
    if list_products:
        markup = pagination_keyboard(list_products, current_page=1, type_callback=2)
        await message.answer('Выберите приём пищи для удаления:', reply_markup=markup)
        await state.update_data(user_id_for_delete_meal=user_id_for_delete_meal)
        await state.set_state(DeleteMeal.USER_ID_FOR_DELETE)
    else:
        await message.answer('У вас отсутствуют приёмы пищи.')
########################################################################################################################
# AddProduct
class Product(StatesGroup):
    NAME = State()
    CALORIES = State()
    PROTEINS = State()
    FATS = State()
    CARBOHYDRATES = State()
    END = State()


@router.message(F.text == 'Добавить продукт')
async def add_product(message: Message, state: FSMContext):
    await message.answer('Введите название продукта.')
    await state.set_state(Product.NAME)


@router.message(Product.NAME)
async def get_name_product(message: Message, state: FSMContext):
    product_name = sub(r'[^\w\d\s\-/%,]', '', message.text)
    await message.answer(f'Название продукта - {product_name}. Теперь введите кол-во калорий на 100 грамм.')
    await state.update_data(product_add_name=product_name)
    await state.set_state(Product.CALORIES)


@router.message(Product.CALORIES)
async def get_calories_product(message: Message, state: FSMContext):
    try:
        calories = int(ceil(float(sub(r'[,]', '.', message.text))))
        await message.answer(f'Калории: {calories}. Теперь введите кол-во белков на 100 грамм.')
        await state.update_data(calories=calories)
        await state.set_state(Product.PROTEINS)
    except:
        await message.answer('Укажите корректное число.')


@router.message(Product.PROTEINS)
async def get_calories_product(message: Message, state: FSMContext):
    try:
        proteins = int(ceil(float(sub(r'[,]', '.', message.text))))
        await message.answer(f'Белки: {proteins}. Теперь введите кол-во жиров на 100 грамм.')
        await state.update_data(proteins=proteins)
        await state.set_state(Product.FATS)
    except:
        await message.answer('Укажите корректное число.')


@router.message(Product.FATS)
async def get_calories_product(message: Message, state: FSMContext):
    try:
        fats = int(ceil(float(sub(r'[,]', '.', message.text))))
        await message.answer(f'Жиры: {fats}. Теперь введите кол-во углеводов на 100 грамм.')
        await state.update_data(fats=fats)
        await state.set_state(Product.CARBOHYDRATES)
    except:
        await message.answer('Укажите корректное число.')


@router.message(Product.CARBOHYDRATES)
async def get_calories_product(message: Message, state: FSMContext):
    try:
        carbohydrates = int(ceil(float(sub(r'[,]', '.', message.text))))
        await state.update_data(carbohydrates=carbohydrates)
        await state.set_state(Product.END)

        data = await state.get_data()

        markup = add_product_keyboard()
        await message.answer(f'Продукт: {data["product_add_name"]}\n'
                             f'\n'
                             f'На 100 грамм:\n'
                             f'Калории: {data["calories"]}\n'
                             f'Белки: {data["proteins"]}\n'
                             f'Жиры: {data["fats"]}\n'
                             f'Углеводы: {data["carbohydrates"]}', reply_markup=markup)
    except:
        await message.answer('Укажите корректное число.')
########################################################################################################################
# DeleteProduct
class DeleteProduct(StatesGroup):
    USER_ID_FOR_DELETE = State()


@router.message(F.text == 'Удалить продукт')
async def delete_meal(message: Message, state: FSMContext):
    user_id_for_delete_meal = message.from_user.id

    list_products = await products_user_from_db(user_id=message.from_user.id)
    if list_products:
        markup = pagination_keyboard(list_products, current_page=1, type_callback=3)
        await message.answer('Выберите продукт для удаления:', reply_markup=markup)
        await state.update_data(user_id_for_delete=user_id_for_delete_meal)
        await state.set_state(DeleteProduct.USER_ID_FOR_DELETE)
    else:
        await message.answer('У вас отсутствуют добавленные продукты.')
########################################################################################################################
# Calendar
class Calendar(StatesGroup):
    USER_ID_FOR_CALENDAR = State()


@router.message(F.text == 'Календарь')
async def calendar(message: Message, state: FSMContext):
    markup = calendar_keyboard()
    await message.answer('Выберите срок, за который хотите узнать последние приёмы пищи:', reply_markup=markup)
    user_id = message.from_user.id
    await state.update_data(user_id_for_calendar=user_id)
    await state.set_state(Calendar.USER_ID_FOR_CALENDAR)