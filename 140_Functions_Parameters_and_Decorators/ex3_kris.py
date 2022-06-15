from psutil._common import memoize

@memoize
def lucas(n):
    if n == 0:
        return 2
    elif n == 1:
        return 1
    else:
        return int(lucas(n-1) + lucas(n-2))


def prime_factors(n):
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(str(i))
    if n > 1:
        factors.append(str(n))
    separator = '*'
    return print("{} = {}". format(n, separator.join(factors)))


prime_factors(lucas(60))
prime_factors(lucas(61))
