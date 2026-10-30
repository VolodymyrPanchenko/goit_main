import timeit
import random
from statistics import median

# ====== Твої алгоритми без змін ======
def insertion_sort(lst):
    lst = lst.copy()
    for i in range(1, len(lst)):
        key = lst[i]
        j = i-1
        while j >= 0 and key < lst[j]:
            lst[j+1] = lst[j]
            j -= 1
        lst[j+1] = key
    return lst

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]
    return merge(merge_sort(left_half), merge_sort(right_half))

def merge(left, right):
    merged = []
    left_index = 0
    right_index = 0
    while left_index < len(left) and right_index < len(right):
        if left[left_index] <= right[right_index]:
            merged.append(left[left_index])
            left_index += 1
        else:
            merged.append(right[right_index])
            right_index += 1
    while left_index < len(left):
        merged.append(left[left_index])
        left_index += 1
    while right_index < len(right):
        merged.append(right[right_index])
        right_index += 1
    return merged

# ====== Початкові тести (залишаю як є) ======
random.seed(42)
small_data = [5, 3, 8, 4, 2]
medium_data = [random.randint(1, 100) for _ in range(100)]
large_data = [random.randint(1, 1000) for _ in range(1000)]

print("📊 ПОРІВНЯННЯ ШВИДКОСТІ")
print("=" * 50)

def run_timer(stmt, number=1000):
    # median з декількох прогонів зменшує шум
    reps = 5
    times = [timeit.timeit(stmt, number=number) for _ in range(reps)]
    return median(times)

print(f"\n🔸 Малий масив ({len(small_data)} елементів):")
time1 = run_timer(lambda: insertion_sort(small_data), number=10000)
time2 = run_timer(lambda: merge_sort(small_data),     number=10000)
time3 = run_timer(lambda: sorted(small_data),         number=10000)
print(f"insertion_sort: {time1:.4f} сек")
print(f"merge_sort:     {time2:.4f} сек")
print(f"sorted():       {time3:.4f} сек")

print(f"\n🔸 Середній масив ({len(medium_data)} елементів):")
time1 = run_timer(lambda: insertion_sort(medium_data), number=1000)
time2 = run_timer(lambda: merge_sort(medium_data),     number=1000)
time3 = run_timer(lambda: sorted(medium_data),         number=1000)
print(f"insertion_sort: {time1:.4f} сек")
print(f"merge_sort:     {time2:.4f} сек")
print(f"sorted():       {time3:.4f} сек")

print(f"\n🔸 Великий масив ({len(large_data)} елементів):")
time1 = run_timer(lambda: insertion_sort(large_data), number=100)
time2 = run_timer(lambda: merge_sort(large_data),     number=100)
time3 = run_timer(lambda: sorted(large_data),         number=100)
print(f"insertion_sort: {time1:.4f} сек")
print(f"merge_sort:     {time2:.4f} сек")
print(f"sorted():       {time3:.4f} сек")

print(f"\n🏆 РЕЙТИНГ ЗА ШВИДКІСТЮ (для великих масивів):")
results = [
    ("sorted()", time3),
    ("merge_sort", time2),
    ("insertion_sort", time1)
]
results.sort(key=lambda x: x[1])
for i, (name, t) in enumerate(results, 1):
    print(f"{i}. {name}: {t:.4f} сек")

# ====== ДОДАТКОВІ СЦЕНАРІЇ ВХІДНИХ ДАНИХ ======
def make_random(n, lo=1, hi=10_000):
    return [random.randint(lo, hi) for _ in range(n)]

def make_sorted(n):
    return list(range(n))

def make_reversed(n):
    return list(range(n, 0, -1))

def make_nearly_sorted(n, swaps= int(0.01 * 10_000)):  # ~1% випадкових перестановок
    arr = list(range(n))
    swaps = max(1, int(0.01 * n))  # 1% елементів поміняти місцями
    for _ in range(swaps):
        i = random.randrange(n)
        j = random.randrange(n)
        arr[i], arr[j] = arr[j], arr[i]
    return arr

def make_half_sorted(n):
    # Перша половина відсортована, друга — випадкова
    half = n // 2
    return list(range(half)) + [random.randint(1, 10_000) for _ in range(n - half)]

SCENARIOS = {
    "random": make_random,
    "sorted": make_sorted,
    "reversed": make_reversed,
    "nearly_sorted": make_nearly_sorted,
    "half_sorted": make_half_sorted,
}

ALGS = [
    ("insertion_sort", insertion_sort),
    ("merge_sort",     merge_sort),
    ("sorted()",       sorted),
]

def bench_scenarios(n_sizes=(100, 1000, 5000)):
    print("\n" + "=" * 50)
    print("🧪 ДОДАТКОВІ СЦЕНАРІЇ ВХІДНИХ ДАНИХ")
    print("=" * 50)
    for n in n_sizes:
        print(f"\n➡️ Розмір N={n}")
        base_data = {name: gen(n) for name, gen in SCENARIOS.items()}
        # Налаштуємо кількість повторів під розмір
        if n <= 200:
            number = 3000
        elif n <= 1000:
            number = 500
        elif n <= 5000:
            number = 50
        else:
            number = 5
        # Замір
        for scen, data in base_data.items():
            print(f"\n  Сценарій: {scen}")
            rows = []
            for alg_name, alg_fn in ALGS:
                t = run_timer(lambda d=data: alg_fn(d), number=number)
                rows.append((alg_name, t))
            rows.sort(key=lambda x: x[1])
            for rank, (alg_name, t) in enumerate(rows, 1):
                print(f"    {rank}. {alg_name:<14} {t:.6f} сек (×{number})")

bench_scenarios((100, 1000, 5000))
