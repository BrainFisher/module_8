import pickle
import os


class Contact:
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone


class AddressBook:
    def __init__(self):
        self.contacts = []

    def add_contact(self, name, phone):
        self.contacts.append(Contact(name, phone))

    def list_contacts(self):
        for contact in self.contacts:
            print(f"Name: {contact.name}, Phone: {contact.phone}")


def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()


def main():
    filename = "addressbook.pkl"
    book = load_data(filename)

    while True:
        print("\n1. Add Contact")
        print("2. List Contacts")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter name: ")
            phone = input("Enter phone number: ")
            book.add_contact(name, phone)
            print("Contact added successfully.")

        elif choice == "2":
            print("\nList of contacts:")
            book.list_contacts()

        elif choice == "3":
            save_data(book, filename)
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
