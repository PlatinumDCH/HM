from faker import Faker
from part_two.crv.models import Contact
from random import choice # exemple variant

def create_contact(value=10):
    faker = Faker()

    fake_contacts = [
        Contact(
            fullname=faker.name(),
            email=faker.email(),
            phone_number=faker.phone_number(),
            preferred_contact_method=choice(['email', 'sms']),
            additional_info=faker.text()).save()
            for _ in range(value)
    ]
    return fake_contacts