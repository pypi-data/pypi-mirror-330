# Negative Binom

A binomial function that extends the domain of combinations to include negative integers.

## Installation
You can install the package using:
```bash
pip install negative-binom
```

## Usage
Import the function and use it as follows:
```python
from negative_binom import binom

# Standard case:
print(binom(5, 2)) # Output: 10

# Extended cases:
print(binom(-5, 2)) # Output: 15
print(binom(5, -2)) # Output: 0
print(binom(-5, -2)) # Output: 0
```

## Mathematical Explanation
The binomial coefficient is traditionally defined as:
```math
\binom{m}{n} = \frac{m!}{n!(m-n)!}, \quad \text{for }m \geq n \geq 0
```
The `binom` function extends the definition to handle negative values of m and n using "The Pascal Hexagon" provided by Hilton and Pedersen in [Extending the Binomial Coefficients to Preserve Symmetry and Pattern](https://doi.org/10.1016/B978-0-08-037237-2.50013-1):

<img src="pascals_hexagon.png" width="450" alt="Pascal's Hexagon"/>

The hexagon is broken into different parts depending on if they contain zeros or non-zeros. Formulas below then can be used to determine the values of the binomial coefficients:

1. Standard case $` (m \geq 0) `$
- If $` m \geq n \geq 0 `$:
```math
\binom{m}{n}=\frac{m!}{n!(m-n)!}
```

- Otherwise:
```math
\binom{m}{n}=0
```
2. Extended case $` (0 > m) `$
- If $` n \geq 0 `$:
```math
\binom{m}{n}=(-1)^n \binom{-m+n-1}{n}
```

- If $` m \geq n `$:
```math
\binom{m}{n}=(-1)^{m+n} \binom{-n-1}{-m-1}
```

- Otherwise:
```math
\binom{m}{n}=0
```

This extended definition of binomial coefficients makes it possible to work with negative values of $` m `$ and $` n `$.

## Personal Notes
I made this package because I needed a binomial function that included negative arguments as well. `math.comb` results in error and `scipy.stats.binom` sets the result to 0 for negative arguments, so they didn't work for me. Hope this helps anyone else.

## License
MIT License