from crv.config import BASE_URL, next_page_url
from crv.content_page import get_page_content
from crv.parsing.parsing_element import parse_author_details

def get_author_details(author_url: str) -> dict[str, str]:
    content = get_page_content(BASE_URL + author_url)
    return parse_author_details(content)

def get_data_author()->list[dict[str,str]]:
    current_page_url = next_page_url
    result = []
    has_next_page = True
    while has_next_page:
        content = get_page_content(BASE_URL + current_page_url)
        for div in content.find_all("div", class_="quote"):
            author_url = div.find('a')['href']
            author_details = get_author_details(author_url)
            result.append(author_details)

        nex_button = content.find('li', class_='next')
        if nex_button:
            current_page_url = nex_button.find('a')['href']
        else:
            has_next_page = False
    return result
