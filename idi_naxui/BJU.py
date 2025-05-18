import requests
from bs4 import BeautifulSoup

def get_bju(url):
    try:
        response = requests.get(
            url,
            headers = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0'
        )
    except:
        return FileNotFoundError ('Эндпоинт недоступен!!!!!!!!!')
    with open('idi_naxui/БЖУ/{}.html', 'w', encoding='utf-8') as file:
        scr = file.write(response.text)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    