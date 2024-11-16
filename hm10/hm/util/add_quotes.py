from bson import ObjectId
from connect import connect_mongo, uri
import json
from pymongo import MongoClient
client = MongoClient(
    uri
)
db = client.hm

with open ('quotes.json', 'r', encoding='utf8') as fd:
    quotes = json.load(fd)

for quote in quotes:
    author = db.autor.find_one({'fullname': quote['author']})
    if author:
        db.quotes.insert_one({
            'quote':quote['quote'],
            'tags':quote['tags'],
            'author': ObjectId(author['_id'])
        })