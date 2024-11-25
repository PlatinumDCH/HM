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