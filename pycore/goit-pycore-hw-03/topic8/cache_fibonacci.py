def caching_fibonacci():
    # Створюємо кеш для збереження обчислених значень
    cache = {}

    def fibonacci(n):
        # Якщо значення вже є у кеші, повертаємо його
        if n in cache:
            return cache[n]
        # Базові випадки
        if n <= 0:
            result = 0
        elif n == 1:
            result = 1
        else:
            # Рекурсивно обчислюємо попередні два числа
            result = fibonacci(n - 1) + fibonacci(n - 2)
        # Запам'ятовуємо результат у кеші
        cache[n] = result
        return result

    return fibonacci


fib = caching_fibonacci()
print(fib(10))   # Виведе 55
print(fib(15))   # Виведе 610    
