from crv.config import BASE_URL, next_page_url
from crv.content_page import get_page_content
from crv.parsing.parsing_element import parse_quotes

def get_data_quotes():
    """main function for parsing quotes"""
    current_page_url = next_page_url
    result = []
    has_next_page = True
    while has_next_page :
        content = get_page_content(BASE_URL+current_page_url)

        for quote_div in content.find_all('div', class_='quote'):
            quote_details = parse_quotes(quote_div)
            result.append(quote_details)


        nex_button = content.find('li',class_='next')
        if nex_button:
            current_page_url = nex_button.find('a')['href']
        else:
            has_next_page = False

    return result

