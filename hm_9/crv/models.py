from mongoengine import *

class Autor(Document):
    fullname = StringField(required=True, max_length=255)
    born_date = StringField(required=True)
    born_location = StringField(required=True, max_length=255)
    description = StringField(required=True)


class Quote(Document):
    tags = ListField(StringField(max_length=50))
    author = ReferenceField(Autor, required=True)
    quote = StringField(required=True)

    meta = {'allow_inheritance': True}


class TextPost(Quote):
    content = StringField()


class ImagePost(Quote):
    image_path = StringField()


class LinkPost(Quote):
    link_url = StringField()