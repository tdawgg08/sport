from math import ceil

from sqlalchemy import func, Table, MetaData, Column, Integer, VARCHAR, Float, select, and_, BigInteger, union_all, \
    DateTime, Text, delete
from database.database import AsyncSessionLocal

metadata = MetaData()

products = Table(
    "products",
    metadata,
Column("id", Integer, primary_key=True, unique=True, nullable=False, autoincrement=True),
    Column("user_id", BigInteger, nullable=False),
    Column("product_name", VARCHAR(255), nullable=False),
    Column("calories", Float, nullable=False),
    Column("proteins", Float, nullable=False),
    Column("fats", Float, nullable=False),
    Column("carbohydrates", Float, nullable=False),
)

consumption = Table('consumption',
    metadata,
    Column('id', Integer, primary_key=True, unique=True, nullable=False, autoincrement=True),
    Column('user_id', BigInteger, nullable=False),
    Column('day', DateTime, nullable=False, default=func.current_timestamp()),
    Column('meal_name', VARCHAR(100), nullable=False),
    Column('product_list', Text, nullable=False),
    Column('weight', Integer, nullable=False),
    Column('calories_result', Integer, nullable=False),
    Column('proteins_result', Integer, nullable=False),
    Column('fats_result', Integer, nullable=False),
    Column('carbohydrates_result', Integer, nullable=False),
)


async def products_from_db(keyword: str, user_id: int) -> list:
    search_words = keyword.lower().split()
    conditions = [func.lower(products.c.product_name).ilike(f'%{word}%') for word in search_words]
    base_query = select(products).where(and_(*conditions), products.c.user_id == 1)

    if user_id != 1:
        user_products_query = select(products).where(and_(*conditions), products.c.user_id == user_id)
        query = union_all(user_products_query, base_query)
    else:
        query = base_query

    async with AsyncSessionLocal() as db_session:
        result = await db_session.execute(query)
        rows = result.fetchall()
        list_found_products = [row.product_name for row in rows]
        return list_found_products


async def meals_from_db(user_id: int) -> list:
    query = select(consumption.c.meal_name).where(consumption.c.user_id == user_id)

    async with AsyncSessionLocal() as db_session:
        result = await db_session.execute(query)
        rows = result.fetchall()
        list_found_meals = [row.meal_name for row in rows]
        return list_found_meals

async def products_user_from_db(user_id: int) -> list:
    query = select(products.c.product_name).where(products.c.user_id == user_id)

    async with AsyncSessionLocal() as db_session:
        result = await db_session.execute(query)
        rows = result.fetchall()
        list_found_products = [row.product_name for row in rows]
        return list_found_products


async def delete_meal_from_db(user_id: int, meal_name: str):
    query = delete(consumption).where(
        (consumption.c.user_id == user_id) &
        (consumption.c.meal_name == meal_name)
    )

    async with AsyncSessionLocal() as db_session:
        await db_session.execute(query)
        await db_session.commit()


async def delete_product_from_db(user_id: int, product_name: str):
    query = delete(products).where(
        (products.c.user_id == user_id) &
        (products.c.product_name == product_name)
    )

    async with AsyncSessionLocal() as db_session:
        await db_session.execute(query)
        await db_session.commit()


async def convert_weight_product(name_product: str, weight: float) -> dict:
    query = select(products).where(products.c.product_name == name_product)
    async with AsyncSessionLocal() as db_session:
        result = await db_session.execute(query)
        product = result.fetchone()

        calories_per_100g = product[3]
        proteins_per_100g = product[4]
        fats_per_100g = product[5]
        carbohydrates_per_100g = product[6]

        calories = ceil((calories_per_100g / 100) * weight)
        proteins = ceil((proteins_per_100g / 100) * weight)
        fats = ceil((fats_per_100g / 100) * weight)
        carbohydrates = ceil((carbohydrates_per_100g / 100) * weight)

        product_info = {
            'product_name': name_product,
            'calories': calories,
            'proteins': proteins,
            'fats': fats,
            'carbohydrates': carbohydrates
        }

        return product_info