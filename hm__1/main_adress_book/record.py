from typing import Optional
from fields import Name, Birthday, Phone


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones: list[Phone] = []  # type: ignore
        self.birthday: Optional[Birthday] = None  # type: ignore

    def add_birthday(self, birthday_str: str) -> None:
        self.birthday = Birthday(birthday_str)

    def add_phone(self, phone) -> None:
        self.phones.append(Phone(phone))

    def remove_phone(self, phone) -> None:
        remove_phone = self.find_phone(phone)
        if remove_phone:
            self.phones.remove(remove_phone)
        else:
            return None

    def find_phone(self, phone: str) -> Optional[Phone]:
        result = [ph for ph in self.phones if ph.value == phone]
        return result[0] if result else None

    def __str__(self):
        phones = ", ".join([str(phone) for phone in self.phones])
        birthday_str = f", Birthday: {self.birthday.value}" if self.birthday else ""
        return f"Contact name: {self.name}, Phones: {phones}{birthday_str}"

    def edit_phone(self, old_phone: str, new_phone: str):
        for index, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[index] = Phone(new_phone)
                return
        raise ValueError("Old phone not found")
