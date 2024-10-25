from collections import UserDict
from record import Record
from datetime import datetime, timedelta


class AddressBook(UserDict):

    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name: str):
        record = self.data.pop(name, None)
        if record:
            del record

    def get_upcoming_birthdays(self):
        today = datetime.now().date()
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday:
                birthday_date = record.birthday.value
                birthday_this_year = self._get_birthday_this_year(birthday_date, today)

                if self._is_upcoming_birthday(birthday_this_year, today):
                    birthday_to_congratulate = self._adjust_for_weekend(
                        birthday_this_year
                    )
                    upcoming_birthdays.append(
                        {
                            "name": record.name.value,
                            "birthday": birthday_to_congratulate,
                        }
                    )
        return upcoming_birthdays

    def _get_birthday_this_year(self, birthday_str, today):
        birthday = datetime.strptime(birthday_str, "%d.%m.%Y").date()
        birthday_this_year = birthday.replace(year=today.year)
        if birthday_this_year < today:
            birthday_this_year = birthday.replace(year=today.year + 1)
        return birthday_this_year

    def _is_upcoming_birthday(self, birthday_this_year, today):
        return 0 <= (birthday_this_year - today).days <= 7

    def _adjust_for_weekend(self, birthday_this_year):
        if birthday_this_year.weekday() >= 5:
            return birthday_this_year + timedelta(
                days=(7 - birthday_this_year.weekday())
            )
        return birthday_this_year

    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())
