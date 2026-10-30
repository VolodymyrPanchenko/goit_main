import re

def generator_numbers(text: str):
    pattern = r"\b\d+\.\d+\b"
    matches = re.findall(pattern, text)
    for item in matches:
        yield item

def sum_profit(text, sum_function = lambda x: x):
    sum_profit = 0
    for item in sum_function(text):
        sum_profit = sum_profit + float(item)
    return sum_profit
            
text = "Загальний дохід працівника складається з декількох частин: 1000.01 як основний дохід, доповнений додатковими надходженнями 27.45 і 324.00 доларів."
total_income = sum_profit(text, generator_numbers)
print(f"Загальний дохід: {total_income}")