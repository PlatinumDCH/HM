import requests
from bs4 import BeautifulSoup

def get_page_content(url):
    response = requests.get(url)
    content = BeautifulSoup(response.content, 'html.parser')
    return content

