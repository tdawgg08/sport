from bs4 import BeautifulSoup
import json
import os

# Основная папка для хранения данных
BASE_DIR = 'idi_naxui'
os.makedirs(BASE_DIR, exist_ok=True)

with open(f'{BASE_DIR}/checker.html', encoding='utf-8') as file:
    scr = file.read()

soup = BeautifulSoup(scr, 'lxml')

categories = {}
current_category = None

# Парсинг данныx
for element in soup.find_all(True):
    if element.name == 'h2' and 'Таблица калорийности:' in element.text:
        current_category = element.get_text(strip=True).replace('Таблица калорийности: ', '')
        categories[current_category] = []
    elif element.name == 'ul' and 'product' in element.get('class', []):
        for item in element.find_all('li'):
            product_data = {
                'name': item.a.get_text(strip=True),
                'link': "https://calorizator.ru/" + item.a['href'],
                'class': item['class'][0]
            }
            if current_category:
                categories[current_category].append(product_data)

# Сохранение в отдельные папки
for category_name, products in categories.items():
    # Создаем безопасное имя для папки
    safe_dirname = ''.join(c for c in category_name if c.isalnum() or c in (' ', '_')).rstrip().replace(' ', '_')
    category_dir = os.path.join(BASE_DIR, 'categories', safe_dirname)
    
    # Создаем папку категории
    os.makedirs(category_dir, exist_ok=True)
    
    # Сохраняем данные
    filepath = os.path.join(category_dir, 'products.json')
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False, indent=2)
    
    print(f"Создана папка: {safe_dirname} | Продуктов: {len(products)}")

# Сохраняем общий отчет в отдельной папке
report_dir = os.path.join(BASE_DIR, 'reports')
os.makedirs(report_dir, exist_ok=True)

report = {
    "total_cateФgories": len(categories),
    "total_products": sum(len(p) for p in categories.values())
}

with open(os.path.join(report_dir, 'summary.json'), 'w', encoding='utf-8') as f:
    json.dump(report, f, indent=2)

print(f"\nИтог:")
print(f"Категорий: {len(categories)}")
print(f"Всего продуктов: {report['total_products']}")
print(f"Отчет сохранен в: {report_dir}/summary.json")