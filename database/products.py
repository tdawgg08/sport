import os
from re import sub
import requests
import bs4
from sqlalchemy import text
from database.database import AsyncSessionLocal, engine
from database.models import Products
from database.orm import Base
import asyncio


url = 'https://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie'

headers = {'Accept': '*/*',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 OPR/102.0.0.0 (Edition Yx GX)'}

req = requests.get(url, headers=headers)
src = req.text

with open('site.html', 'w', encoding='utf-8-sig') as full_site:
    full_site.write(src)

with open('site.html', 'r', encoding='utf-8-sig') as full_site:
    src = full_site.read()

soup = bs4.BeautifulSoup(src, 'lxml')
all_products_hrefs = soup.find_all(class_='mzr-tc-group-item-href')

async def process_and_insert_data():
    with open('site.html', 'r', encoding='utf-8-sig') as full_site:
        src = full_site.read()
    soup = bs4.BeautifulSoup(src, 'lxml')
    headers = {'Accept': '*/*',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 OPR/102.0.0.0 (Edition Yx GX)'}
    all_products_hrefs = soup.find_all(class_='mzr-tc-group-item-href')
    async with engine.begin() as conn:
        # Удаляем ВСЕ таблицы с каскадом
        await conn.execute(text("DROP TABLE IF EXISTS users, user_callories, products, sub_categories, categories CASCADE"))
        # Создаем таблицы заново
        await conn.run_sync(Base.metadata.create_all)


    for el in all_products_hrefs:
        url = 'https://health-diet.ru' + el.get('href')
        req = requests.get(url, headers=headers)
        src = req.text
        soup = bs4.BeautifulSoup(src, 'lxml')
        try:
            products = soup.find(class_="mzr-tc-group-table").find('tbody').find_all('tr')
        except:
            continue
        for item in products:
            product_data = item.find_all('td')

            product_name = sub(r'[^\w\d\s\-/%,]', '', product_data[0].find('a').text.lower())
            calories = float(product_data[1].text.split(' ')[0].replace(',', '.'))
            proteins = float(product_data[2].text.split(' ')[0].replace(',', '.'))
            fats = float(product_data[3].text.split(' ')[0].replace(',', '.'))
            carbohydrates = float(product_data[4].text.split(' ')[0].replace(',', '.'))

            async with AsyncSessionLocal() as db:
                product = Products(
                    user_id=1,
                    product_name=product_name,
                    calories=calories,
                    proteins=proteins,
                    fats=fats,
                    carbohydrates=carbohydrates
                )

                db.add(product)
                await db.commit()

    os.remove('site.html')

