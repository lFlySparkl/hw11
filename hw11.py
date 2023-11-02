from collections import UserDict
from datetime import datetime
import re


class Field:
    # setter та getter логіку для атрибутів value спадкоємців Field.
    def __init__(self, value):
        self.__privat_value = None
        self.value = value

    @property
    def value(self):
        return self.__privat_value

    @value.setter
    def value(self, value: str):
        if value.isalpha():
            self.__privat_value = value
        else:
            raise Exception("Wrong value")


class Name(Field):
    def self_name(self, name):
        self.__privat_name = None
        self.name = name
        return str(self.name)

    @property
    def name(self):
        return self.__privat_name

    @name.setter
    def name(self, name: str):
        if name.isalpha():
            self.__privat_name = name
        else:
            raise Exception("Wrong name")


class Phone(Field):
    def __init__(self, value):
        self.__privat_value = None
        self.value = value

    @property
    def value(self):
        return self.__privat_value

    @value.setter
    def value(self, value: str) -> None:
        if len(value) == 10 and value.isdigit():
            self.__privat_value = value
        else:
            raise ValueError("Phone number most be 10 didgit")


class Birthday(Field):
    def __init__(self, birthday) -> None:
        self.__privat_birthday = None
        self.birthday = birthday

    @property
    def birthday(self):
        return self.__privat_birthday

    @birthday.setter
    def birthday(self, birthday):
        if not self.is_date(self, birthday):
            self.__privat_birthday = birthday
        else:
            ValueError("Invalid phone number format"),

            TypeError("Dont birtday")

    def is_date(self, birthday: str) -> None:
        patern_birth = r"^(1|2)(9|0)[0-2,7-9][0-9]{1}(.|/| )(0|1)[0-9](.|/| )[0-3][0-9]"
        return bool(re.match(patern_birth, birthday))


class Record:
    # Додамо поле для дня народження Birthday. Це поле не обов'язкове, але може бути тільки одне.
    # Перевірку на коректність веденого номера телефону setter для value класу Phone.
    # Перевірку на коректність веденого дня народження setter для value класу Birthday.

    # Клас Record приймає ще один додатковий (опціональний) аргумент класу Birthday
    # Додамо функціонал роботи з Birthday у клас Record, а саме функцію days_to_birthday,
    # яка повертає кількість днів до наступного дня народження.
    # Клас Record реалізує метод days_to_birthday, який повертає кількість днів до наступного дня народження контакту,
    # якщо день народження заданий.

    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday

    def add_phone(self, value: Field):
        self.phones.append(value)

    def remove_phone(self, number):
        if number in self.phones:
            self.phones.remove(number)
        else:
            raise ValueError

    def edit_phone(self, old_number, new_number):
        if old_number in self.phones:
            idx = ""
            for number in self.phones:
                if number == old_number:
                    idx = self.phones.index(number)
            self.phones[idx] = new_number

        else:
            raise ValueError

    def find_phone(self, number):
        if number in self.phones:
            self.value = number
            return self
        else:
            return None

    def days_to_birthday(self, birthday: Birthday):
        self.birthday = birthday
        date_split = datetime.strptime(
            birthday.replace(" ", "-").replace(".", "-"), "%d-%m-%Y"
        )
        new_date_of_bd = date_split.replace(
            year=datetime.today().year, month=date_split.month, day=date_split.day
        )
        result = new_date_of_bd.date() - datetime.today().date()
        return result.days

    def __str__(self):
        if Birthday.birthday:
            return f"Contact name: {self.name.value}, phones: {'; '.join(p for p in self.phones)}, birth: {self.birthday} ({self.days_to_birthday(self.birthday)} day to birthday)"
        else:
            return f"Contact name: {self.name.value}, phones: {'; '.join(p for p in self.phones)}"


class AddressBook(UserDict):
    # Додамо пагінацію (посторінковий висновок) для AddressBook для ситуацій,
    # коли книга дуже велика і треба показати вміст частинами, а не все одразу. Реалізуємо це через створення ітератора за записами.
    # AddressBook реалізує метод iterator,
    # який повертає генератор за записами AddressBook і за одну ітерацію повертає уявлення для N записів.

    def add_record(self, contact: Record):
        self.data[contact.name.value] = contact

    def find(self, name):
        if name in self.data:
            return self.data[name]
        else:
            return None

    def delete(self, contact):
        if contact in self.data:
            return self.data.pop(contact)
        else:
            return None

class Iterator:
    MAX_VALUE = 0

    def __init__(self, adressBook):
        self.current_value = 0
        self.adressBook = AddressBook
        self.MAX_VALUE = len(adressBook.data)

    def __next__(self):
        if self.current_value < self.MAX_VALUE:
            self.current_value += 1
            return self.adressBook.data[self.current_value]
        raise StopIteration

if __name__ == "__main__":
    book = AddressBook()
    john_record = Record("John")
    john_record.add_phone("5555555555")
    john_record.add_phone("1234567890")
    book.add_record(john_record)
    john_record.days_to_birthday("05-11-1976")
    john_record
    book.add_record(john_record)
    john_record
    print(john_record)
    jane_record = Record("Jane")
    jane_record.days_to_birthday("03.11.2002")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)
    print(jane_record)
    john = book.find("John")
    john_record.edit_phone("1234567890", "1112223333")
    john_record.find_phone("5555555555")
    john_record.find_phone("1234567890")
    found_phone2 = john_record.find_phone("1112223333")
