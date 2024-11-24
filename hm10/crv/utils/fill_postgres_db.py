from connect import connect_pymongo
import psycopg2

mongo_db = connect_pymongo()
author_collection = mongo_db['autor']
quote_collection = mongo_db['quotes']

pg_conn = psycopg2.connect(
    dbname = 'postgres',
    user = 'postgres',
    password = 'saksaganskogo22',
    host = 'localhost',
    port = '5432'
)

pg_cursor = pg_conn.cursor()

# Создание таблиц в PostgreSQL
create_author_table = """
CREATE TABLE IF NOT EXISTS author (
    id SERIAL PRIMARY KEY,
    _id VARCHAR(24) UNIQUE,
    fullname TEXT,
    born_date TEXT,
    born_location TEXT,
    description TEXT
);
"""
create_quote_table = """
CREATE TABLE IF NOT EXISTS quotes (
    id SERIAL PRIMARY KEY,
    _id VARCHAR(24) UNIQUE,
    quote TEXT,
    tags TEXT[],
    author_id INTEGER,
    FOREIGN KEY (author_id) REFERENCES author (id)
);
"""

pg_cursor.execute(create_author_table)
pg_cursor.execute(create_quote_table)
pg_conn.commit()

try:
    authors = list(author_collection.find())
except TypeError as e:
    print(f"Ошибка при вызове find на author_collection: {e}")
    raise

author_map = {}

for author in authors:
    author_id = author['_id']
    author_data = (
        str(author_id),
        author.get('fullname', ''),
        author.get('born_date', ''),
        author.get('born_location', ''),
        author.get('description', '')
    )
    pg_cursor.execute("""
           INSERT INTO author (_id, fullname, born_date, born_location, description)
           VALUES (%s, %s, %s, %s, %s) RETURNING id;
       """, author_data)
    author_map[str(author_id)] = pg_cursor.fetchone()[0]

pg_conn.commit()

# Получение цитат из MongoDB
try:
    quotes = list(quote_collection.find())
except TypeError as e:
    print(f"Ошибка при вызове find на quote_collection: {e}")
    raise

for quote in quotes:
    quote_id = quote["_id"]
    author_id = quote["author"]
    quote_data = (
        str(quote_id),
        quote.get("quote", ""),
        quote.get("tags", []),
        author_map[str(author_id)]
    )
    pg_cursor.execute("""
        INSERT INTO quotes (_id, quote, tags, author_id)
        VALUES (%s, %s, %s, %s);
    """, quote_data)

pg_conn.commit()

# Закрытие соединений
pg_cursor.close()
pg_conn.close()

