import re
from collections import UserDict
from datetime import datetime, date, timedelta


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, name):
        if not name:
            raise ValueError("Name cannot be empty")
        super().__init__(name)


class Phone(Field):
    def __init__(self, phone):
        pattern = r'^\d{10}$'
        if not (re.match(pattern, str(phone))):
            raise ValueError('Phone number is not valid')
        super().__init__(phone)


class Birthday(Field):
    def __init__(self, value):
        try:
            birthday = datetime.strptime(value, "%d.%m.%Y").date()
            super().__init__(birthday)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    # def __str__(self):
    #     return self.value.strftime("%d.%m.%Y")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        phone_number = Phone(phone)
        self.phones.append(phone_number)

    def find_phone(self, phone):
        for phone_number in self.phones:
            if phone_number.value == phone:
                return phone_number
        return None

    def remove_phone(self, phone):
        phone_number = self.find_phone(phone)
        self.phones.remove(phone_number)

    def edit_phone(self, old_phone, new_phone):
        old_phone_number = self.find_phone(old_phone)
        if old_phone_number is None:
            raise ValueError("Phone number not found")
        new_phone_number = Phone(new_phone)
        old_phone_number.value = new_phone_number.value

    def add_birthday(self, birthday):
        birthday_date = Birthday(birthday)
        self.birthday = birthday_date

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday.value if self.birthday else "unknown."}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        self.data.pop(name, None)

    @staticmethod
    def _find_next_weekday(start_date, weekday):
        days_ahead = weekday - start_date.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        return start_date + timedelta(days=days_ahead)

    @staticmethod
    def _adjust_for_weekend(birthday):
        if birthday.weekday() >= 5:
            return AddressBook._find_next_weekday(birthday, 0)
        return birthday

    def get_upcoming_birthdays(self, days=7):
        upcoming_birthdays = []
        today = date.today()

        for record in self.data.values():
            if record.birthday is None:
                continue

            birthday_this_year = record.birthday.value.replace(year=today.year)

            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)
                # next_birthday = birthday_this_year.replace(year=today.year + 1)
                # next_birthday = self._adjust_for_weekend(next_birthday)
                # upcoming_birthdays.append({"name": record.name.value, "birthday": next_birthday.strftime("%d.%m.%Y")})
            if 0 <= (birthday_this_year - today).days <= days:
                birthday_this_year = self._adjust_for_weekend(birthday_this_year)
                upcoming_birthdays.append(
                    {"name": record.name.value, "birthday": birthday_this_year.strftime("%d.%m.%Y")})

        return upcoming_birthdays

    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())
