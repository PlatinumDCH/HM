import requests
from bs4 import BeautifulSoup


def get_page_content(url:str, parser:str = 'lxml')->BeautifulSoup:
    response = requests.get(url)
    content = BeautifulSoup(response.content, parser)
    return content

