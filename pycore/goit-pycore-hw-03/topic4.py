from datetime import datetime
import random
import re
from datetime import datetime, timedelta

def get_days_from_today(date_str):
    date = datetime.strptime(date_str, "%Y-%m-%d")
    current_date = datetime.today()
    days_difference = current_date - date
    return days_difference.days

# print(get_days_from_today("2025-06-13"))


def get_numbers_ticket(start, end, quantity):
    if quantity > (end - start + 1):
        print("Кількість чисел більша за доступний діапазон")
        return []
    numbers = random.sample(range(start, end + 1), quantity)
    return numbers

# lottery_numbers = get_numbers_ticket(1, 49, 6)
lottery_numbers = get_numbers_ticket(10, 11, 6)
# print("Ваші лотерейні числа:", lottery_numbers)

def normalize_phone(phone_number):
    default_prefix="+38"
    # pattern = r"(\d{3})-(\d{3})-(\d{4})"
    # replacement = r"(\1) \2-\3"
    cleaned = re.sub(r"[^\d+]", "", phone_number)
    if not cleaned.startswith("+"):
        if not cleaned.startswith("38"):
            cleaned = default_prefix + cleaned
        else:
            cleaned = "+" + cleaned
#    formatted_phone = re.sub(pattern, replacement, phone_number)
    return cleaned

raw_numbers = [
    "067\\t123 4567",
    "(095) 234-5678\\n",
    "+380 44 123 4567",
    "380501234567",
    "    +38(050)123-32-34",
    "     0503451234",
    "(050)8889900",
    "38050-111-22-22",
    "38050 111 22 11   ",
]

# sanitized_numbers = [normalize_phone(num) for num in raw_numbers]
# print("Нормалізовані номери телефонів для SMS-розсилки:", sanitized_numbers)
users = [
    {"name": "John Doe", "birthday": "1985.01.23"},
    {"name": "Jane Smith", "birthday": "1990.01.27"}
]    

def get_upcoming_birthdays(users):
    upcoming = []
    today = datetime.strptime("2024.01.22", "%Y.%m.%d")  # for test, in real should be   today = datetime.today()
   
    for user in users:
        birthday = datetime.strptime(user["birthday"], "%Y.%m.%d")
        birthday_this_year = birthday.replace(year=today.year)

        if birthday_this_year < today:
            birthday_this_year = birthday_this_year.replace(year=today.year + 1)

        days_diff = (birthday_this_year - today).days

        if 0 < days_diff <= 7:
            greeting_date = birthday_this_year

            if greeting_date.weekday() in [5, 6]:  # субота або неділя
                days_to_monday = 7 - greeting_date.weekday()
                greeting_date += timedelta(days=days_to_monday)

            upcoming.append({
                "name": user["name"],
                "congratulation_date": greeting_date.strftime("%Y.%m.%d")
            })

    return upcoming

    # print(get_upcoming_birthdays(users))