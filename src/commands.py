from models import Record, AddressBook
from utils import input_error


@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = f"Contact {name} updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = f"Contact {name} added."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError(name)
    record.edit_phone(old_phone, new_phone)
    return f"Contact {name} updated."


@input_error
def print_phone_numbers(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError(name)
    phones = record.phones
    return f"Contact {name} phones: {'; '.join(p.value for p in phones) if phones else 'No available phone numbers.'}"


@input_error
def print_all_contacts(book: AddressBook):
    if not book.data:
        return "No contacts found"
    return book


@input_error
def add_birthday(args, book: AddressBook):
    name, birthday, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError(name)
    record.add_birthday(birthday)
    return f"Birthday to contact {name} added."


@input_error
def show_birthday(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError(name)
    birthday = record.birthday
    return f"Birthday of {name} is {birthday if birthday else 'unknown.'}"


@input_error
def birthdays(book: AddressBook):
    upcoming_birthdays = book.get_upcoming_birthdays()
    if not upcoming_birthdays:
        return "No upcoming birthdays in the next 7 days."

    result = list()
    for birthday in upcoming_birthdays:
        result.append(f"Contact {birthday['name']} birthday is {birthday['birthday']}")
    return "\n".join(result)
