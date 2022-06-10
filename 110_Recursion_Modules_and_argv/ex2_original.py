import re
import sys

counts = {}

for line in sys.stdin:
    for word in re.findall(r'[a-z\']+', line.lower()):
        counts[word] = counts.get(word, 0) + 1
        for word, count in sorted(counts.items()):
            print(word, count)


# NOTHING TO DO WITH THIS FILE
