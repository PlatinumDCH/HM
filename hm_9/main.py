from get_quotes import get_data_quotes
from get_author import get_data_author
from crv.json_load import save_to_json

def main():
    save_to_json(get_data_quotes(),'quotes.json')
    save_to_json(get_data_author(),'authors.json')

if __name__ == '__main__':
    main()