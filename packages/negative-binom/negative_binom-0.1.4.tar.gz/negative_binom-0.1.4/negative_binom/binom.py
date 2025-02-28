from math import comb


def binom(m, n):
    if m >= 0:
        if n < 0 or m < n:
            return 0
        else:
            return comb(m, n)
    else:
        if n >= 0:
            return int((-1) ** n * comb(-m + n - 1, n))
        elif n <= m:
            return int((-1) ** (m + n) * comb(-n - 1, -m - 1))
        else:
            return 0
