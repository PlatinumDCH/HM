from configuration.models import Autor,Quote
from connection import connect_to_db

connect_to_db()

FORMAT = 'utf-8'

author_aliases = {
    'al': 'Albert Einstein',
    'st': 'Steve Martin'
}

tag_aliases = {
    'li': 'life'
}
def search_by_author(author_name: str) -> list:

    if author_name.lower() in author_aliases:
        author_name = author_aliases[author_name.lower()]


    authors = Autor.objects(
        fullname__iexact=author_name
    )
    if authors:
        author_ids = [author.id for author in authors]
        quotes = Quote.objects(
            author__in=author_ids
        ).all()
        return quotes
    return []

def search_by_tag(tag: str) -> list:

    if tag.lower() in tag_aliases:
        tag = tag_aliases[tag.lower()]

    quotes = Quote.objects(
        tags__icontains=tag
    ).all()
    return quotes


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
                        print(quote.quote)#.encode(FORMAT))
                else:
                    print(f'No quotes found for author: {value}')

            case 'tag':
                quotes = search_by_tag(value)
                if quotes:
                    for quote in quotes:
                        print(quote.quote)#.encode(FORMAT))
                else:
                    print(f'No quotes found for tag: {value}')
            case 'tags':
                quotes = search_by_set_tag(value)
                if quotes:
                    for quote in quotes:
                        print(quote.quote)#.encode(FORMAT))
                else:
                    print(f'No quotes found for tags: {value}')


            case _:
                print('Invalid command')

if __name__ == '__main__':
    main()




