import random
import matplotlib.pyplot as plt

def monte_carlo_dice(trials=100_000):
    """Симуляція кидків двох кубиків методом Монте-Карло."""
    counts = {s: 0 for s in range(2, 13)}

    # Симуляція кидків
    for _ in range(trials):
        roll_sum = random.randint(1, 6) + random.randint(1, 6)
        counts[roll_sum] += 1

    # Обчислення ймовірностей
    probs = {s: counts[s] / trials for s in counts}
    return probs

def print_results(probs):
    """Виводить таблицю ймовірностей та порівняння з теоретичними."""
    print(f"{'Сума':<5} | {'Монте-Карло (%)':<15} | {'Теорія (%)':<12} | Різниця (в.п.)")
    print("-" * 55)
    
    theoretical = {
        2: 1/36, 3: 2/36, 4: 3/36, 5: 4/36, 6: 5/36,
        7: 6/36, 8: 5/36, 9: 4/36, 10: 3/36, 11: 2/36, 12: 1/36
    }

    for s in range(2, 13):
        emp = probs[s] * 100
        theo = theoretical[s] * 100
        diff = abs(emp - theo)
        print(f"{s:<5} | {emp:<15.2f} | {theo:<12.2f} | {diff:.3f}")

def plot_results(probs):
    """Будує графік порівняння емпіричних і теоретичних ймовірностей."""
    sums = list(probs.keys())
    emp_values = [probs[s] for s in sums]
    theoretical = [ (6 - abs(7 - s)) / 36 for s in sums ]

    plt.bar(sums, emp_values, alpha=0.7, label="Монте-Карло")
    plt.plot(sums, theoretical, "o-", color="red", label="Теоретичний розподіл")
    plt.xlabel("Сума на двох кубиках")
    plt.ylabel("Ймовірність")
    plt.title("Порівняння розподілів Монте-Карло та теоретичного")
    plt.xticks(sums)
    plt.legend()
    plt.show()

# ---- Запуск програми ----
if __name__ == "__main__":
    N = 100_000
    probs = monte_carlo_dice(N)
    print(f"Результати симуляції {N} кидків двох кубиків:\n")
    print_results(probs)
    plot_results(probs)
