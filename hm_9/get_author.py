from crv.config import BASE_URL, next_page_url
from crv.content_page import get_page_content




def get_author_details(author_url):
    content = get_page_content(BASE_URL+author_url)
    fullname = content.find("h3", class_="author-title").get_text(strip=True)
    born_date = content.find("span", class_="author-born-date").get_text(strip=True)
    born_location = content.find("span", class_="author-born-location").get_text(strip=True)
    description = content.find("div", class_="author-description").get_text(strip=True)

    return {
        "fullname": fullname,
        "born_date": born_date,
        "born_location": born_location,
        "description": description
    }

def get_data_author():
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
