from pymongo import MongoClient


uri = "mongodb+srv://plarium:cHL93W33OpxFNUM2@cluster0.lsq3b.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
def check_connect():
    try:

        db = get_mongo_db()
        print("Connection [TRUE].")
        return db
    except ConnectionError as e:
        print(f"Connection [FALSE]{e}")

def get_mongo_db():
    client = MongoClient(
        uri
    )
    db = client.hm
    return db


def print_quotes():
    db = check_connect()
    if db is not None:
        quotes_collection = db['quote']
        quotes = quotes_collection.find()
        for x in quotes:
            print(x)

if __name__ == '__main__':

    print_quotes()