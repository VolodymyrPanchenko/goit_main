import numpy as np
import matplotlib.pyplot as plt
from math import sqrt
import scipy.integrate as spi

# --- Функція та межі інтегрування ---
def f(x):
    return x**2

a, b = 0.0, 2.0

# --- Обчислення за допомогою SciPy quad ---
quad_val, quad_err = spi.quad(f, a, b)

# --- Метод Монте-Карло ---
def monte_carlo_integral(n):
    rng = np.random.default_rng(42)
    xs = rng.uniform(a, b, size=n)
    fx = f(xs)
    est = (b - a) * fx.mean()
    se = (b - a) * fx.std(ddof=1) / sqrt(n)
    return est, se

# Обчислення
N = 100_000
mc_est, mc_se = monte_carlo_integral(N)

# --- Виведення результатів ---
print("=" * 50)
print("Інтегрування f(x) = x² на [0, 2]")
print("=" * 50)
print(f"SciPy quad (еталон):      {quad_val:.10f}")
print(f"Монте-Карло (N={N}):      {mc_est:.10f}")
print(f"Стандартна похибка МК:    {mc_se:.6f}")
print(f"Абсолютна різниця:        {abs(mc_est - quad_val):.10f}")
print(f"Відносна похибка:         {abs(mc_est - quad_val) / quad_val * 100:.4f}%")
print("=" * 50)

# --- Дослідження збіжності ---
print("\nЗбіжність методу Монте-Карло:")
print("-" * 50)
print(f"{'N':<10} {'Оцінка':<15} {'Похибка':<15}")
print("-" * 50)

for n in [100, 1_000, 10_000, 100_000]:
    est, _ = monte_carlo_integral(n)
    error = abs(est - quad_val)
    print(f"{n:<10} {est:<15.8f} {error:<15.8f}")