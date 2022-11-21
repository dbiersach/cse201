# euler_gamma.py

import numpy as np


def factorial_recursive(n):
    if n == 0:
        return 1
    else:
        return int(n) * factorial_recursive(n - 1)


def f(x, s):
    try:
        return np.power(x, s - 1) * np.exp(-x)
    except ZeroDivisionError:
        return 0


def simpsons_rule(fn, s, a, b, intervals):
    dx = (b - a) / intervals
    area = fn(a, s) + fn(b, s)
    for i in range(1, int(intervals)):
        area += fn(a + i * dx, s) * (2 * (i % 2 + 1))
    return dx / 3 * area


def euler_gamma(s):
    return simpsons_rule(f, s, 0, 1e3, 1e5)


def factorial_gamma(x):
    return euler_gamma(x + 1)


def main():
    print(f"{'n':>10}", end="")
    print(f"{'Factorial (Recursive)':>23}", end="")
    print(f"{'Factorial (Gamma)':>21}")

    for n in range(11):
        print(f"{n:>10}", end="")
        print(f"{factorial_recursive(n):>23,.0f}", end="")
        print(f"{factorial_gamma(n):>21,.0f}")

    print()
    print(f"Estimate: (1/2)! = {factorial_gamma(1/2):0.4f}")
    print(f"Exact:    (1/2)! = {np.sqrt(np.pi)/2:0.4f}")


main()
