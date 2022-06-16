"""
The program has the timer activated for the first task.
 The memoization is commented. Should be uncommented
for the next task.
"""

import time
from psutil._common import memoize


class timer(object):
    def __init__(self, f):
        self.f = f
        self.active = False

    def __call__(self, *args):
        if self.active:
            return self.f(*args)
        start = time.time()
        self.active = True
        res = self.f(*args)
        end = time.time()
        self.active = False
        return "The result is {} and it took {} second/s".format(res, round(end - start, 2))


@timer
# @memoize #Caches values in order to save iterations and make function faster
def lucas(n):
    if n == 0:
        return 2
    elif n == 1:
        return 1
    else:
        return int(lucas(n - 1) + lucas(n - 2))


"""
Another way for Lucas numbers. Works much faster.
"""
# def lucas(n, a=2, b=1):
#     return lucas(n - 1, b, a + b) if n else a


print(lucas(60))

print(lucas(100))
