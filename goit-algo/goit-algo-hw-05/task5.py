import timeit
import re
from pathlib import Path

# ===================== Алгоритми пошуку =====================

def polynomial_hash(s, base=256, modulus=101):
    """
    Повертає поліноміальний хеш рядка s.
    """
    n = len(s)
    hash_value = 0
    for i, char in enumerate(s):
        power_of_base = pow(base, n - i - 1, modulus)
        hash_value = (hash_value + ord(char) * power_of_base) % modulus
    return hash_value


def rabin_karp_search(main_string, substring):
    substring_length = len(substring)
    main_string_length = len(main_string)

    if substring_length == 0:
        return 0
    if substring_length > main_string_length:
        return -1

    base = 256
    modulus = 101

    substring_hash = polynomial_hash(substring, base, modulus)
    current_slice_hash = polynomial_hash(main_string[:substring_length], base, modulus)

    h_multiplier = pow(base, substring_length - 1) % modulus

    for i in range(main_string_length - substring_length + 1):
        if substring_hash == current_slice_hash:
            if main_string[i:i + substring_length] == substring:
                return i

        if i < main_string_length - substring_length:
            current_slice_hash = (current_slice_hash - ord(main_string[i]) * h_multiplier) % modulus
            current_slice_hash = (current_slice_hash * base + ord(main_string[i + substring_length])) % modulus
            if current_slice_hash < 0:
                current_slice_hash += modulus

    return -1


def build_shift_table(pattern):
    """
    Створити таблицю зсувів для алгоритму Боєра-Мура.
    """
    table = {}
    length = len(pattern)
    if length == 0:
        return table
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
    table.setdefault(pattern[-1], length)
    return table


def boyer_moore_search(text, pattern):
    if len(pattern) == 0:
        return 0
    if len(pattern) > len(text):
        return -1

    shift_table = build_shift_table(pattern)
    i = 0

    while i <= len(text) - len(pattern):
        j = len(pattern) - 1

        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1

        if j < 0:
            return i

        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))

    return -1


def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps


def kmp_search(main_string, pattern):
    M = len(pattern)
    N = len(main_string)

    if M == 0:
        return 0
    if M > N:
        return -1

    lps = compute_lps(pattern)

    i = j = 0

    while i < N:
        if pattern[j] == main_string[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1

        if j == M:
            return i - j

    return -1


# ===================== Бенчмарк функции =====================

def time_algorithm(func, text, pattern, number=100):
    """
    Вимірює час виконання алгоритму
    """
    return timeit.timeit(lambda: func(text, pattern), number=number) / number


def benchmark_algorithms(text, existing_word, missing_word, text_name):
    """
    Тестує всі три алгоритми на даному тексті
    """
    algorithms = {
        "Боєра-Мура": boyer_moore_search,
        "КМП": kmp_search,
        "Рабіна-Карпа": rabin_karp_search
    }
    
    print(f"\n=== {text_name} ===")
    print(f"Довжина тексту: {len(text)} символів")
    print(f"Шукаємо існуюче слово: '{existing_word}'")
    print(f"Шукаємо неіснуюче слово: '{missing_word}'")
    
    # Перевіряємо, що слова коректні
    assert existing_word in text, f"Слово '{existing_word}' не знайдено в тексті!"
    assert missing_word not in text, f"Слово '{missing_word}' знайдено в тексті!"
    
    results = {}
    
    for name, algo in algorithms.items():
        # Тест з існуючим словом
        time_existing = time_algorithm(algo, text, existing_word, number=100)
        pos_existing = algo(text, existing_word)
        
        # Тест з неіснуючим словом  
        time_missing = time_algorithm(algo, text, missing_word, number=100)
        pos_missing = algo(text, missing_word)
        
        results[name] = {
            'existing': time_existing,
            'missing': time_missing
        }
        
        print(f"\n{name}:")
        print(f"  Існуюче слово: {time_existing:.8f} сек (позиція: {pos_existing})")
        print(f"  Неіснуюче слово: {time_missing:.8f} сек (результат: {pos_missing})")
    
    return results


def main():
    # Завантажуємо файли
    try:
        with open('txt/стаття 1.txt', 'r', encoding='utf-8') as f:
            text1 = f.read()
        with open('txt/стаття 2.txt', 'r', encoding='utf-8') as f:
            text2 = f.read()
    except FileNotFoundError:
        print("Помістіть файли 'стаття 1.txt' та 'стаття 2.txt' в папку 'txt/'")
        return
    
    # Обираємо слова для тестування (захардкожено)
    # Для файлу 1 (стаття про алгоритми)
    existing_word1 = "алгоритмів"  # це слово є в тексті
    missing_word1 = "ксилофонистка"  # слово, якого точно немає
    
    # Для файлу 2 (стаття про рекомендаційні системи)
    existing_word2 = "рекомендаційної"  # це слово є в тексті  
    missing_word2 = "флейтарика"  # слово, якого точно немає
    
    # Запускаємо бенчмарки
    results1 = benchmark_algorithms(text1, existing_word1, missing_word1, "Стаття 1")
    results2 = benchmark_algorithms(text2, existing_word2, missing_word2, "Стаття 2")
    
    # Загальні результати
    print("\n" + "="*50)
    print("ЗВЕДЕННЯ РЕЗУЛЬТАТІВ")
    print("="*50)
    
    all_results = {}
    for algo in ["Боєра-Мура", "КМП", "Рабіна-Карпа"]:
        total_time = (results1[algo]['existing'] + results1[algo]['missing'] + 
                     results2[algo]['existing'] + results2[algo]['missing'])
        all_results[algo] = total_time
        print(f"{algo}: {total_time:.8f} сек (загальний час по всіх тестах)")
    
    fastest = min(all_results.items(), key=lambda x: x[1])
    print(f"\nНАЙШВИДШИЙ АЛГОРИТМ: {fastest[0]} ({fastest[1]:.8f} сек)")


if __name__ == "__main__":
    main()