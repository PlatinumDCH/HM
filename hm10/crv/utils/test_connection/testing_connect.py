from crv.utils.connect import connect_pymongo



def fetch_all_authors():
    db = connect_pymongo()
    authors_collections = db['autor']
    authors = authors_collections.find()
    for x in authors:
        print(x)


fetch_all_authors()