from typing import Dict, Tuple, List

Item = Dict[str, int]
Items = Dict[str, Item]
Selection = Dict[str, Item]

items: Items = {
    "pizza": {"cost": 50, "calories": 300},
    "hamburger": {"cost": 40, "calories": 250},
    "hot-dog": {"cost": 30, "calories": 200},
    "pepsi": {"cost": 10, "calories": 100},
    "cola": {"cost": 15, "calories": 220},
    "potato": {"cost": 25, "calories": 350},
}

def summarize(selection: Selection) -> Tuple[int, int]:
    """Повертає (загальні_калорії, загальна_вартість)."""
    total_cal = sum(v["calories"] for v in selection.values())
    total_cost = sum(v["cost"] for v in selection.values())
    return total_cal, total_cost


def greedy_algorithm(items: Items, budget: int) -> Tuple[Selection, int, int]:
    """
    Жадібний підхід: сортуємо за спаданням (calories/cost), 
    далі додаємо поки вкладаємося в бюджет.
    """
    # Сортуємо за ratio, а при рівності — за калорійністю (щоб брати «поживніші»)
    order = sorted(
        items.items(),
        key=lambda kv: (kv[1]["calories"] / kv[1]["cost"], kv[1]["calories"]),
        reverse=True,
    )

    chosen: Selection = {}
    spent = 0
    for name, it in order:
        if spent + it["cost"] <= budget:
            chosen[name] = it
            spent += it["cost"]

    total_cal, total_cost = summarize(chosen)
    return chosen, total_cal, total_cost


def dynamic_programming(items: Items, budget: int) -> Tuple[Selection, int, int]:
    """
    Класичний 0/1-рюкзак (ДП): O(N * budget) по часу і O(N * budget) по пам'яті.
    За однакової калорійності — віддаємо перевагу меншій вартості.
    """
    names: List[str] = list(items.keys())
    n = len(names)

    # dp[c] = (калорії, маска_вибору_бітами, вартість)
    # Зберігаємо ще й вартість, щоб при рівних калоріях обирати дешевший набір
    dp = [(-10**9, 0, 0)] * (budget + 1)  # заповнюємо «мінус нескінченність»
    dp[0] = (0, 0, 0)

    for i, name in enumerate(names):
        cost_i = items[name]["cost"]
        cal_i = items[name]["calories"]
        # Ідемо справа-наліво, щоб кожен елемент брали не більше одного разу
        for c in range(budget, cost_i - 1, -1):
            prev_cal, prev_mask, prev_cost = dp[c - cost_i]
            cand_cal = prev_cal + cal_i
            cand_cost = prev_cost + cost_i
            cand_mask = prev_mask | (1 << i)

            best_cal, best_mask, best_cost = dp[c]
            # Краще за більшою калорійністю, або при рівній — за меншою вартістю
            if (cand_cal > best_cal) or (cand_cal == best_cal and cand_cost < best_cost):
                dp[c] = (cand_cal, cand_mask, cand_cost)

    # Знаходимо найкраще по всіх c ≤ budget
    best = max(
        (dp[c] for c in range(budget + 1)),
        key=lambda t: (t[0], -t[2])  # більше калорій, за рівності — менша вартість
    )
    best_cal, best_mask, best_cost = best

    # Відновлюємо вибрані позиції
    selection: Selection = {}
    for i, name in enumerate(names):
        if best_mask & (1 << i):
            selection[name] = items[name]

    return selection, best_cal, best_cost


# --------------------- Приклад використання ---------------------
if __name__ == "__main__":
    for B in [50, 75, 85, 90, 100, 115, 150]:
        g_sel, g_cal, g_cost = greedy_algorithm(items, B)
        d_sel, d_cal, d_cost = dynamic_programming(items, B)

        print(f"\nБюджет: {B}")
        print(f"  Greedy  -> калорії: {g_cal:4d}, вартість: {g_cost:3d}, набір: {list(g_sel.keys())}")
        print(f"  DP(opt) -> калорії: {d_cal:4d}, вартість: {d_cost:3d}, набір: {list(d_sel.keys())}")
