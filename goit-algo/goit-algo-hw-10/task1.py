import time
from statistics import mean, stdev

COINS = [50, 25, 10, 5, 2, 1]

def find_coins_greedy(amount: int, coins=COINS):
    """Жадібний алгоритм: завжди беремо найбільший можливий номінал."""
    if amount < 0:
        raise ValueError("amount must be non-negative")
    result = {}
    remaining = amount
    for c in sorted(coins, reverse=True):
        if remaining == 0:
            break
        take = remaining // c
        if take:
            result[c] = take
            remaining -= take * c
    return result

def find_min_coins(amount: int, coins=COINS):
    """Динамічне програмування: мінімальна кількість монет."""
    if amount < 0:
        raise ValueError("amount must be non-negative")
    n = amount
    max_val = float('inf')
    dp = [0] + [max_val] * n
    parent = [0] * (n + 1)

    for a in range(1, n + 1):
        best = max_val
        best_coin = 0
        for c in coins:
            if c <= a and dp[a - c] + 1 < best:
                best = dp[a - c] + 1
                best_coin = c
        dp[a] = best
        parent[a] = best_coin

    if dp[n] == max_val:
        return {}

    res = {}
    a = n
    while a > 0:
        c = parent[a]
        res[c] = res.get(c, 0) + 1
        a -= c
    return dict(sorted(res.items()))

def benchmark(amounts, rounds=10):
    results = []
    for amt in amounts:
        # Greedy timing
        g_times = []
        for _ in range(rounds):
            t0 = time.perf_counter()
            find_coins_greedy(amt)
            g_times.append(time.perf_counter() - t0)

        # DP timing
        d_times = []
        for _ in range(rounds):
            t0 = time.perf_counter()
            find_min_coins(amt)
            d_times.append(time.perf_counter() - t0)

        results.append({
            "amount": amt,
            "greedy_ms": mean(g_times) * 1000,
            "dp_ms": mean(d_times) * 1000,
            "greedy_sol": find_coins_greedy(amt),
            "dp_sol": find_min_coins(amt),
        })
    return results

if __name__ == "__main__":
    # Приклад для 113
    print("Сума 113:")
    print("Greedy ->", find_coins_greedy(113))
    print("DP     ->", find_min_coins(113))

    # Бенчмарки
    amounts = [113, 999, 10_000, 50_000]
    rows = benchmark(amounts)
    print("\nБенчмарки (середнє за 10 запусків):")
    print(f"{'Amount':>8} | {'Greedy (ms)':>12} | {'DP (ms)':>12}")
    for r in rows:
        print(f"{r['amount']:>8} | {r['greedy_ms']:12.4f} | {r['dp_ms']:12.4f}")
