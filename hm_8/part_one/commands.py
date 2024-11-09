import sys
from part_one.search import search_by_author, search_by_set_tag, search_by_tag

FORMAT = 'utf-8'
if sys.stdout.encoding != FORMAT:
    sys.stdout.reconfigure(encoding=FORMAT)

def execute_command(command: str, value: str):
    match command:
        case 'name':
            quotes = search_by_author(value)
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