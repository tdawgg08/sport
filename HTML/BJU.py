import os
import json
from bs4 import BeautifulSoup






def parse_local_html(file_path):
    """Парсинг данных из локального HTML-файла"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл {file_path} не найден!")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'lxml')
    
    products = []
    
    # Находим все строки таблицы
    for row in soup.find_all('tr', class_=lambda x: x in ['odd', 'even']):
        try:
            # Извлекаем данные из ячеек
            cells = row.find_all('td')
            
            product = {
                'name': cells[1].a.text.strip(),
                'protein': cells[2].text.strip(),
                'fat': cells[3].text.strip(),
                'carbohydrate': cells[4].text.strip(),
                'calories': cells[5].text.strip(),
                'image': cells[0].a['href'],
                'link': 'https://calorizator.ru' + cells[1].a['href']
            }
            products.append(product)
        except Exception as e:
            print(f"Ошибка парсинга строки: {str(e)}")
            continue
    
    return products

def save_to_json(data, filename):
    """Сохранение данных в JSON файл"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    # Путь к вашему локальному файлу
    input_file = 'HTML\cccchecker.html'
    output_file = 'parsed_products.json'
    
    if not os.path.exists(input_file):
        print(f"Файл {input_file} не найден!")
        exit()
    
    # Парсим данные
    parsed_data = parse_local_html(input_file)
    
    # Сохраняем результат
    save_to_json(parsed_data, output_file)
    
    print(f"Успешно обработано {len(parsed_data)} продуктов")
    print(f"Результаты сохранены в {output_file}")