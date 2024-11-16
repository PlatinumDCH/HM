from django import template
from bson.objectid import ObjectId

from ..utils import get_mongo_db
register = template.Library()
def get_author(id_):
    db = get_mongo_db()
    author = db.autor.find_one({'_id': ObjectId(id_)})
    return author['fullname']


register.filter('author', get_author)
