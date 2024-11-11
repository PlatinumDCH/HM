def parse_quotes(quote_div):

    quote = quote_div.find('span', class_='text').get_text()
    author = quote_div.find('small', class_='author').get_text(strip=True)
    tags = [tag.get_text(strip=True) for tag in quote_div.find_all('a', class_='tag')]

    return  {
            'tags': tags,
            'author': author,
            'quote': quote,

    }

