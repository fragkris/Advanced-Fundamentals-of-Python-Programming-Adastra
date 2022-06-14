"""
Cheet sheet.
Not required for a task.
"""



a = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
print("Middle two: ", a[3:5])
print("All but ends: ", a[1:7])
print("All: ", a[:])
print("Until fifth: ", a[:5])
print("Everything but last: ", a[:-1])
print("From fourth until end: ", a[4:])
print("Last three: ", a[-3:])
print("From 3rd from end until 2nd from end ", a[-3:-1])
print("Everything but skip every second: ", a[::2])
print("Print all from back and skip every second: ", a[::-2])

# ( from : to : [stride(step)] )


#defaultdict
# def create_author_mapping(cookbooks: List[Cookbook]):
#     counter = defaultdict(Lambda: 0)
#     for cookbook in cookbooks:
#         counter[cookbook.author] += 1
#     return counter