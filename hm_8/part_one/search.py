from configuration.models import Autor,Quote
from configuration.connect import  connect_redis,connect_mongo
from redis_lru import RedisLRU


connect_mongo()
cache = RedisLRU(connect_redis())


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


