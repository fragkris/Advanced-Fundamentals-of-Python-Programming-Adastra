def my_list(n):
    i = 0
    l = []

    while i < n:
        l.append(i)
        i += 1

    return l


# We can change this function
# into a generator function

def my_gen(n):
    i = 1

    while i <= n:
        yield i
        i += 1

g = my_gen(5)

for x in g:
    print(x)