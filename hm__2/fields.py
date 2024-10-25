from datetime import datetime
from exceptions_ import ValidatePhone, ValidatedBirthday


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValidatePhone("Invalid phone number")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value: str):
        try:
            datetime.strptime(value, "%d.%m.%Y")
            super().__init__(value)
        except ValueError:
            raise ValidatedBirthday("Invalid date format. Use DD.MM.YYYY")


class Name(Field):
    def __init__(self, value):
        super().__init__(value)
