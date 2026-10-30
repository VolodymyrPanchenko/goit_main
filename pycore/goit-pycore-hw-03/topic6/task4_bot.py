def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def add_contact(args, contacts):
    if len(args) < 2:
        return "Please provide both name and phone number."
    name, phone = args[0], args[1]
    contacts[name] = phone
    return "Contact added."

def change_contact(args, contacts):
    if len(args) < 2:
        return "Please provide both name and new phone number."
    name, new_phone = args[0], args[1]
    if name in contacts:
        contacts[name] = new_phone
        return f"Contact {name} updated."
    else:
        return f"Contact {name} does not exist. Use 'add' to create a new contact."

def get_all_contacts(contacts):
    if not contacts:
        return "No contacts found."
    return "\n".join(f"{name}: {phone}" for name, phone in contacts.items())

def get_phone(args, contacts):
    if len(args) < 1:
        return "Please specify the contact name."
    
    name = args[0]
    phone = contacts.get(name)
    
    if phone:
        return f"{name}'s phone number is {phone}"
    else:
        return f"No contact found with name '{name}'."

def main():
    contacts = {}
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
            print(add_contact(args, contacts))
        elif command == "change":
             print(change_contact(args, contacts))
        elif command == "phone":
            print(get_phone(args, contacts))        
        elif command == "all":
             print(get_all_contacts(contacts))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()