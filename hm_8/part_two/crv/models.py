from mongoengine import Document, StringField, BooleanField, connect

connect('email_contact_db')
class Contact(Document):
    fullname = StringField(required=True)
    email = StringField(required=True)
    phone_number = StringField(required=True)
    preferred_contact_method = StringField(required=True, choices=['email', 'sms'])

    additional_info = StringField()
    message_sent = BooleanField(default=False)
