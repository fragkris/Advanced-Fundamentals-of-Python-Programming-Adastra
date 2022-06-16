import sys
import random

COUNT = 0
WORDS = []


def generate_permutations(a, n, count):
    global COUNT
    global WORDS
    if n == 0:
        if ''.join(a) not in WORDS:
            WORDS.append(''.join(a))
            print(''.join(a))
            COUNT += random.uniform(0.7, 1)

        """Counter is increasing randomly but close to 1. 
        This way it will most probably not be exactly 20.
        The maximum will be also in the 20-ish range (29),
        in case the random number is always 0.7.
        Since the point of Heap's algorithm is to present only unique 
        combinations, there is a list of words, and a new word is
        printed and added to list only if its not repeated."""

    else:
        for i in range(n):
            generate_permutations(a, n - 1, count)

            j = round(random.uniform(random.random() * 10, len(a) - 1)) \
                if n + (random.uniform(0, 9)) % (random.uniform(0, 9)) == 0 \
                else (i + round(random.uniform(0, len(a) - 2)))
            """In order not to get only the initial ~20 elements, 
            the numbers above will be round random numbers inside the allowed length.
            The if statement is also randomized in order for more unique output."""
            a[j], a[n], = a[n], a[j]

        generate_permutations(a, n - 1, count)
        if COUNT >= count:
            sys.exit(1)


WORD = 'Kris Kotomanov'

generate_permutations(list(WORD), len(WORD) - 1, 20)
