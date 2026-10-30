from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
      def __init__(self, name):
        super().__init__(name)

class Phone(Field):
    def __init__(self, number):
        validated = self.validate(number)
        super().__init__(validated)

    def validate(self, number):
        # Видаляємо пробіли, якщо є
        cleaned = number.strip()
        
        # Перевіряємо, що складається тільки з цифр
        if not cleaned.isdigit():
            raise ValueError("Номер телефону повинен містити тільки цифри.")
        
        # Перевіряємо довжину
        if len(cleaned) != 10:
            raise ValueError("Номер телефону повинен містити рівно 10 цифр.")
        
        return cleaned

    def __str__(self):
        return f"Phone: {self.value}"


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone_str):
        phone = Phone(phone_str)
        self.phones.append(phone)
    def edit_phone(self, old_phone_str, new_phone_str):
        for phone in self.phones:
            if phone.value == old_phone_str:
                phone.value = Phone(new_phone_str).value
                return
        raise ValueError(f"Phone number '{old_phone_str}' not found in record for {self.name.value}.")
    def find_phone(self, phone_str):
        for phone in self.phones:
            if phone.value == phone_str:
                return phone
        return None   

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record):
        self[record.name.value] =record
    def find(self, name):
        return self.data.get(name, None)    
    def delete(self, name):
        if name in self.data:
            del self.data[name]
            print(f"Контакт '{name}' удалён.")
        else:
            print(f"Контакт '{name}' не найден.") 
  # Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

# Додавання запису John до адресної книги
book = AddressBook()
book.add_record(john_record)

# Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)
  # Виведення всіх записів у книзі
for name, record in book.data.items():
    print(record)
# Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")
print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555
# Пошук конкретного телефону у записі John
found_phone = john_record.find_phone("5555555555")
print(f"{john_record.name}: {found_phone}")  # Виведення: 5555555555

# Видалення запису Jane
book.delete("Jane")    
