import sys

def generate_permutations(a, n):
    if n == 0:
        print(''.join(a))
    else:
        for i in range(n):
            generate_permutations(a, n-1)
            j = 0 if n % 2 == 0 else i
            a[j], a[n], = a[n], a[j]
        generate_permutations(a, n-1)

if len(sys.argv) != 2:
    sys.stderr.write('Exactly one argument is required\n')
    sys.exit(1)

word = sys.argv[1]

generate_permutations(list(word), len(word) - 1)
