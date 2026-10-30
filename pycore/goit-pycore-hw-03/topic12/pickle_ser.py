from pathlib import Path
import pickle
from address_book import AddressBook, Record 

FILENAME = "addressbook.pkl"

def save_data(book, filename=FILENAME):
    """Зберігає дані у файл."""
    Path(filename).write_bytes(pickle.dumps(book))
    print(f"✅ Адресна книга збережена у {filename}")

def load_data(filename=FILENAME):
    """
    Завантажує дані з файлу.
    Якщо файл відсутній або пошкоджений, створює нову порожню адресну книгу.
    """
    path = Path(filename)
    if not path.exists():
        print(f"⚠️ Файл {filename} не знайдено. Створюю нову адресу книгу.")
        return AddressBook()
    try:
        return pickle.loads(path.read_bytes())
    except (pickle.UnpicklingError, Exception) as e:
        print(f"⚠️ Помилка при завантаженні файлу {filename}: {e}")
        print("🆕 Створюю нову порожню адресу книгу.")
        return AddressBook()

if __name__ == "__main__":
    # Завантажуємо існуючі дані або створюємо нову книгу
    book = load_data()
    print("🔄 Дані після завантаження/створення:")
    for name, record in book.data.items():
        print(record)

    # Додаємо записи

    # Запис для John
    john = Record("John")
    john.add_phone("1234567890")
    john.add_phone("5555555555")
    john.add_birthday("15.04.1990")
    book.add_record(john)

    # Запис для Jane
    jane = Record("Jane")
    jane.add_phone("9876543210")
    jane.add_birthday("22.08.1985")
    book.add_record(jane)

    # Запис для Bob без телефонів
    bob = Record("Bob")
    book.add_record(bob)

    # Зберігаємо створені записи
    save_data(book)

    # Завантажуємо дані ще раз для перевірки
    loaded_book = load_data()
    print("🔄 Завантажені дані після збереження:")
    for name, record in loaded_book.data.items():
        print(record)
