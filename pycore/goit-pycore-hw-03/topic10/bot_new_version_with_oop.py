import datetime
from address_book import AddressBook, Name, Phone, Birthday, Record


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return "Please provide a valid command with arguments."
        except ValueError as e:
             return str(e)
        except AttributeError as e:
             return str(e)
    return inner

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, book):
    # if len(args) < 2:
    #     return "Please provide both name and phone number."
    name, phone = args[0], args[1]
    record = Record(name)
    record.add_phone(phone)
    book.add_record(record)
    # contacts[name] = phone
    return "Contact added."

def get_all_contacts(book):
    if not book.data:
        return "No contacts found."
    
    result = []
    for name, record in book.data.items():
        phones = ", ".join(phone.value for phone in record.phones)
        result.append(f"{name}: {phones}")
    
    return "\n".join(result)
 
@input_error
def change_phone(args, book):
    # if len(args) < 2:
    #     return "Please provide both name and new phone number."
    name, old_phone, new_phone = args[0], args[1], args[2]
    record = book.find(name)
    if record is None:        
        return f"Contact {name} does not exist. Use 'add' to create a new contact."     
    else:
        record.edit_phone(old_phone, new_phone)
        return f"Contact {name} updated."

@input_error
def add_birthday(args, book):
    # if len(args) < 2:
    #     return "Please provide both name and new phone number."
    name, birthday = args[0], args[1]
    record = book.find(name)
    if record is None:        
        return f"Contact {name} does not exist. Use 'add' to create a new contact."     
    else:
        record.add_birthday(birthday)
        return f"Birthday for {name} added."    

@input_error
def show_birthday(args, book):
    # if len(args) < 2:
    #     return "Please provide both name and new phone number."
    name = args[0]
    record = book.find(name)
    if record is None:        
        return f"Contact {name} does not exist. Use 'add' to create a new contact."     
    else:
        if record.birthday:
            return f"{name}'s birthday is {record.birthday.value}."
        else:
            return f"{name} does not have a birthday set."  

def birthdays(book):
    if not book.data:
        return "No contacts found."
    
    result = []
    for name, record in book.data.items():
        if record.birthday:
            result.append(f"{name}: {record.birthday.value}")
    
    if not result:
        return "No birthdays found."
    
    return "\n".join(result)

@input_error
def get_phone(args, contacts):
    # if len(args) < 1:
    #     return "Please specify the contact name."
    
    name = args[0]
    phone = contacts.get(name)
    
    if phone:
        return f"{name}'s phone number is {phone}"
    else:
        return f"No contact found with name '{name}'."
    
def get_upcoming_birthdays(book):
    users = book.data.values()
    upcoming = []
    today = datetime.datetime.strptime("2024.01.22", "%Y.%m.%d")  # for test, in real should be datetime.datetime.today()

    for user in users:
        if not user.birthday:
            continue

        
        birthday_date = user.birthday.value

       
        birthday_this_year = datetime.datetime(
            year=today.year,
            month=birthday_date.month,
            day=birthday_date.day
        )

        if birthday_this_year < today:
            birthday_this_year = birthday_this_year.replace(year=today.year + 1)

        days_diff = (birthday_this_year - today).days

        if 0 < days_diff <= 7:
            greeting_date = birthday_this_year

            if greeting_date.weekday() in [5, 6]:  # суббота или воскресенье
                days_to_monday = 7 - greeting_date.weekday()
                greeting_date += datetime.timedelta(days=days_to_monday)

            upcoming.append({
                "name": user.name.value,
                "congratulation_date": greeting_date.strftime("%Y.%m.%d")
            })

    return upcoming

def main():
#     contacts = {}
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
             print(change_phone(args, book))
        elif command == "phone":
            print(get_phone(args, book))        
        elif command == "all":
             print(get_all_contacts(book))
        elif command == "add-birthday":
             print(add_birthday(args, book))
        elif command == "show-birthday":
             print(show_birthday(args, book))
        elif command == "all_birthdays":
            print(birthdays(book))
        elif command == "birthdays":
            print(get_upcoming_birthdays(book))    
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()