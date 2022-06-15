"""
NOTHING TO DO HERE.
JUST AN EXAMPLE OF WALRUS OPERATOR.
"""

my_list = [1, 2, 3, 4, 5]

if len(my_list) > 3:
    print(f"The list has {len(my_list)} elements")

if (n := len(my_list)) > 3:
    print(f"The list has {n} elements")

