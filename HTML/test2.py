from bs4 import BeautifulSoup
import os

with open('HTML/checker.html', encoding='utf-8') as file:
    scr = file.read()

soup = BeautifulSoup(scr, 'lxml')

categories = {}
current_category = None

def get_category():
    with open('HTML/checker.html', encoding='utf-8') as file:
        scr = file.read()

    soup = BeautifulSoup(scr, 'lxml')

    categories = {}
    current_category = None
    for element in soup.find_all(True):
        if element.name == 'h2' and 'Таблица калорийности: ' in element.text:
            current_category = element.get_text(strip=True).replace('Таблица калорийности: ', '')   
            
            categories[current_category] = []
            
        elif element.name == 'ul' and 'product' in element.get('class'):
            if current_category:
                for item in element.find_all('li'):
                    product_data = {
                        'name': item.a.get_text(strip=True),
                        'link': "https://calorizator.ru/" + item.a['href'],
                        'class': item['class'][0]
                    }
                    if current_category:
                        categories[current_category].append(product_data)

    return categories                        


    # list_category = []
    # for category_name, products in categories.items():
    #     k = ''.join(c for c in category_name if c.isalnum() or c in (' ', '_')).rstrip().replace(' ', '_')
    #     category_dir = f'HTML/categories/{k}'
    #     os.makedirs(category_dir, exist_ok=True)  
    #     with open(f'{category_dir}/Продукты_категории.html', 'w', encoding='utf-8') as f:
    #         for i in products:
    #             f.write(str(f'NAME = {i['name']}, LINK = {i['link']}, Class = {i['class']}\n')) 
    #     list_category.append(k)               
    # return list_category   

if __name__ == '__main__':
    get_category()