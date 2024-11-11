from bs4 import BeautifulSoup


def parse_quotes(quote_div):

    quote = quote_div.find('span', class_='text').get_text()
    author = quote_div.find('small', class_='author').get_text(strip=True)
    tags = [tag.get_text(strip=True) for tag in quote_div.find_all('a', class_='tag')]

    return  {
            'tags': tags,
            'author': author,
            'quote': quote,

    }

def parse_author_details(content: BeautifulSoup) -> dict[str, str]:
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

