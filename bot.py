import pickle
from datetime import datetime, timedelta


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value=None):
        super().__init__(value)

    def validate(self):
        if self.value is not None and (len(self.value) != 10 or not self.value.isdigit()):
            raise ValueError("Номер телефону має містити 10 цифр.")


class Birthday(Field):
    def __init__(self, value=None):
        if value:
            try:
                datetime.strptime(value, "%d.%m.%Y")
            except ValueError:
                raise ValueError(
                    "Неправильний формат дати. Використовуйте DD.MM.YYYY.")
            else:
                super().__init__(value)
        else:
            super().__init__(value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        while True:
            try:
                phone.validate()
                break
            except ValueError as e:
                print("Помилка:", str(e))
                print("Будь ласка, введіть номер у правильному форматі.")
                phone.value = input("Введіть номер телефону: ")

        self.phones.append(phone)

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if str(p) != phone]

    def edit_phone(self, old_phone, new_phone):
        if old_phone not in [str(p) for p in self.phones]:
            raise ValueError("Номер телефону не знайдено.")
        self.remove_phone(old_phone)
        self.add_phone(new_phone)

    def find_phone(self, phone):
        for p in self.phones:
            if str(p) == phone:
                return p.value
        raise ValueError("Номер телефону не знайдено.")

    def __str__(self):
        phones_str = '; '.join(str(p) for p in self.phones)
        return f"Ім'я: {self.name}, Телефони: {phones_str}, День народження: {self.birthday}"


class AddressBook:
    def __init__(self):
        self.data = {}

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        if name not in self.data:
            raise KeyError("Контакт не знайдено.")
        return self.data[name]

    def delete(self, name):
        if name not in self.data:
            raise KeyError("Контакт не знайдено.")

    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        upcoming_birthdays = []

        for record in self.data.values():
            birthday = datetime.strptime(
                record.birthday.value, "%d.%m.%Y").date().replace(year=today.year)

            if birthday < today:
                birthday = birthday.replace(year=today.year + 1)

            days_until_birthday = (birthday - today).days
            if 0 <= days_until_birthday <= 7:
                if birthday.weekday() >= 5:  # Якщо день народження припадає на вихідний
                    # Переносимо на наступний понеділок
                    days_until_birthday += (7 - birthday.weekday())

                congratulation_date = today + \
                    timedelta(days=days_until_birthday)
                upcoming_birthdays.append({
                    "name": record.name.value,
                    "congratulation_date": congratulation_date.strftime("%Y.%m.%d")
                })

        return upcoming_birthdays


class Bot:
    def __init__(self):
        self.users = {}
        self.address_book = load_data()
        self.last_added_dob = None
        self.last_added_phone = None

    def add_user(self, name):
        dob = None
        phone = None

        while True:
            dob_input = input("Введіть дату народження (DD.MM.YYYY): ")
            try:
                dob = Birthday(dob_input)
                break
            except ValueError as e:
                print("Помилка:", str(e))
                print("Будь ласка, введіть дату у правильному форматі.")

        while True:
            phone_input = input("Введіть номер телефону: ")
            try:
                phone = Phone(phone_input)
                break
            except ValueError as e:
                print("Помилка:", str(e))
                print("Будь ласка, введіть номер у правильному форматі.")

        record = Record(name)
        record.birthday = dob
        record.add_phone(phone)

        self.address_book.add_record(record)
        print("Контакт додано успішно.")

    def get_user_info(self, name):
        try:
            record = self.address_book.find(name)
            return str(record)
        except KeyError:
            return "Контакт не знайдено."

    def list_all_users(self):
        if self.address_book.data:
            return "\n".join([record.name.value for record in self.address_book.data.values()])
        else:
            return "Немає доступних контактів."

    def add_birthday(self, name, dob):
        try:
            record = self.address_book.find(name)
            record.birthday = Birthday(dob)
            print(f"День народження додано/оновлено для {name}.")
        except ValueError as e:
            print("Помилка:", str(e))
            print("Будь ласка, введіть дату у правильному форматі.")
        except KeyError:
            print("Контакт не знайдено.")

    def show_birthday(self, name):
        try:
            record = self.address_book.find(name)
            return f"День народження {name} на {record.birthday.value}."
        except KeyError:
            return "Контакт не знайдено."

    def birthdays(self):
        upcoming_birthdays = self.address_book.get_upcoming_birthdays()
        if upcoming_birthdays:
            return "\n".join([f"{birthday['name']} - {birthday['congratulation_date']}" for birthday in upcoming_birthdays])
        else:
            return "Немає наближених днів народження."

    def run(self):
        while True:
            print("\nМеню:")
            print("1. Додати новий контакт")
            print("2. Показати інформацію про контакт")
            print("3. Показати всі контакти")
            print("4. Додати день народження")
            print("5. Показати день народження")
            print("6. Показати наближені дні народження")
            print("7. Вихід")

            choice = input("Введіть ваш вибір: ")

            if choice == "1":
                name = input("Введіть ім'я: ").capitalize()
                self.add_user(name)

            elif choice == "2":
                name = input(
                    "Введіть ім'я для отримання інформації: ").capitalize()
                print(self.get_user_info(name))

            elif choice == "3":
                print("Список контактів:")
                print(self.list_all_users())

            elif choice == "4":
                name = input("Введіть ім'я: ").capitalize()
                dob = input("Введіть дату народження (DD.MM.YYYY): ")
                self.add_birthday(name, dob)

            elif choice == "5":
                name = input("Введіть ім'я: ").capitalize()
                print(self.show_birthday(name))

            elif choice == "6":
                print("Наближені дні народження:")
                print(self.birthdays())

            elif choice == "7":
                save_data(self.address_book)
                print("Виходимо...")
                break

            else:
                print("Неправильний вибір. Будь ласка, спробуйте знову.")


def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено


if __name__ == "__main__":
    bot = Bot()
    bot.run()
