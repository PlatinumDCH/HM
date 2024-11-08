import sys

from configuration.models import Autor,Quote
from configuration.conn_mongo import connect_to_db
from redis_lru import RedisLRU
from configuration.conn_redis import connect_redis_db

FORMAT = 'utf-8'
if sys.stdout.encoding != FORMAT:
    sys.stdout.reconfigure(encoding=FORMAT)

connect_to_db()
cache = RedisLRU(connect_redis_db())


@cache
def search_by_author(author_name: str):
    authors = Autor.objects(fullname__istartswith=author_name)
    if authors:
        author_ids = [author.id for author in authors]
        quotes = Quote.objects(author__in=author_ids)
        quote_list = [
            {'quote':quote.quote,
             'author':quote.author.fullname,
             'tags':quote.tags} for quote in quotes]

        return quote_list
    else:
        print(f"No authors found with names starting with '{author_name}'")
        return []

def search_by_tag(tag: str) -> list:
    quotes = Quote.objects(
        tags__istartswith=tag
    ).all()
    quote_list = [
        {"quote": quote.quote,
         "author": quote.author.fullname,
         "tags": quote.tags} for quote in quotes]

    return quote_list

def search_by_set_tag(tags)->list:

    tags = tags.split(',')
    quotes = Quote.objects(
        tags__in=tags
    ).all()
    return quotes

def main():
    run = True
    while run:
        input_user = input('Enter command: ').strip()

        if input_user.lower() == 'exit':
            run = False
            continue

        if ':' not in input_user:
            print('Invalid input format. Expected "command: value"')
            continue

        command, value = [part.strip() for part in input_user.split(':',maxsplit=1)]

        match command:
            case 'name':
                quotes =  search_by_author(value)
                if quotes:
                    for quote in quotes:
                        print(quote['quote'])
                else:
                    print(f'No quotes found for author: {value}')

            case 'tag':
                quotes = search_by_tag(value)
                if quotes:
                    for quote in quotes:
                        print(quote['quote'])
                else:
                    print(f'No quotes found for tag: {value}')
            case 'tags':
                quotes = search_by_set_tag(value)
                if quotes:
                    for quote in quotes:
                        print(quote['quote'])
                else:
                    print(f'No quotes found for tags: {value}')


            case _:
                print('Invalid command')

if __name__ == '__main__':
    main()




