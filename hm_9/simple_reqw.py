import requests
from bs4 import BeautifulSoup
import time

url  = 'https://dropstab.com'

def get_content(url, parser='html.parser')->BeautifulSoup:
    r = requests.get(url)
    content = BeautifulSoup(r.text, parser)
    return content

for i in range(5):
    content = get_content(url)
    price_element = content.find('span', class_='truncate text-blue-600 dark:text-blue-500')
    price = [element.get_text() for element in price_element]
    print(price)
    time.sleep(1)
