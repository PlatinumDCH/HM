import json
from configuration.connect import connect_mongo
from configuration.models import Autor, Quote
from get_path import DataPath

connect_mongo()


def load_scientists(json_file):
    try:
        with open(json_file, 'r') as file:
            scientists_data = json.load(file)
            for item in scientists_data:
                try:
                    existing_scientist = Autor.objects(fullname=item['fullname']).first()
                    if not existing_scientist:
                        scientist = Autor(
                            fullname=item['fullname'],
                            born_date=item['born_date'],
                            born_location=item['born_location'],
                            description=item['description']
                        )
                        scientist.save()
                        print(f"Created new scientist: {scientist.fullname}")
                except Exception as e:
                    print(f"Error creating scientist {item['fullname']}: {e}")
    except FileNotFoundError:
        print(f"File {json_file} not found.")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from the file {json_file}.")


def load_quotes(json_file):
    try:
        with open(json_file, 'r') as file:
            quotes_data = json.load(file)
            for item in quotes_data:
                try:
                    author = Autor.objects(fullname=item['author']).first()
                    if author:
                        quote = Quote(
                            tags=item['tags'],
                            author=author,
                            quote=item['quote']
                        )
                        quote.save()
                        print(f"Added quote by {author.fullname}")
                    else:
                        print(f"Author {item['author']} not found in the database")
                except Exception as e:
                    print(f"Error adding quote: {e}")
    except FileNotFoundError:
        print(f"File {json_file} not found.")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from the file {json_file}.")



load_scientists(DataPath.AUTHORS.value)
load_quotes(DataPath.QUOTES.value)
