import requests
from bs4 import BeautifulSoup

def get_auto(url):
    req = requests.get(url, headers = {
        'user-agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0'
  }
    )
    with open('idi_naxui/checker.html', encoding='utf-8') as file:
        scr = file.read()
    soup = BeautifulSoup(scr, 'lxml')
    products = soup.find('div', id='main-content', class_='block').find_all('h2')
    for i in products:
        print(i)
    




if __name__ == '__main__':
    get_auto('https://calorizator.ru/product')