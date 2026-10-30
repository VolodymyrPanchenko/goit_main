from collections import UserDict
import datetime

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

    @staticmethod
    def validate(number):
         # Remove spaces, if any
        cleaned = number.strip()
        
        # Check that it consists only of digits
        if not cleaned.isdigit():
            raise ValueError("The phone number must contain digits only.")
        
        # Check the length
        if len(cleaned) != 10:
            raise ValueError("The phone number must contain exactly 10 digits.")
        
        return cleaned

    def __str__(self):
        return f"Phone: {self.value}"

class Birthday(Field):
    def __init__(self, value):
        try:
            # Преобразуем строку в datetime.date
            date_obj = datetime.datetime.strptime(value.strip(), "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        # Сохраняем дату в Field.value
        super().__init__(date_obj)

    def __str__(self):
        # При печати возвращаем дату в формате DD.MM.YYYY
        return self.value.strftime("%d.%m.%Y")
       
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
    # def add_record(self, record):
    #     self[record.name.value] =record
    # def find(self, name):
    #     return self.data.get(name, None)       
    def add_phone(self, phone_str):
        phone = Phone(phone_str)
        self.phones.append(phone)
    def add_birthday(self, birthday_str):
        self.birthday = Birthday(birthday_str)
    def find_phone(self, phone_str):
        for phone in self.phones:
            if phone.value == phone_str:
                return phone
        return None   
    def edit_phone(self, old_phone, new_phone):
        phone_to_edit = self.find_phone(old_phone)
        if phone_to_edit:
            # Validate new phone number
            new_phone_obj = Phone(new_phone)
            # Replace the old phone with new one
            index = self.phones.index(phone_to_edit)
            self.phones[index] = new_phone_obj
            return True
        return False
    def remove_phone(self, phone_str):
        for phone in self.phones:
            if phone.value == phone_str:
                self.phones.remove(phone)
                return
        raise ValueError(f"Phone number '{phone_str}' not found in record for {self.name.value}.")
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
         

