import sys
from collections import defaultdict
import itertools


def pairwise(iterable):
    # pairwise('ABCDEFG') --> AB BC CD DE EF FG
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


infile = "input.txt" if len(sys.argv) == 1 else sys.argv[1]

rules = {}
with open(infile) as inf:
    letters = inf.readline().rstrip("\n")
    for line in inf:
        if not "->" in line:
            continue
        items = line.rstrip("\n").split()
        rules[items[0]] = (items[0][0] + items[2], items[2] + items[0][1])

pairs = defaultdict(int)
for pair in pairwise(letters):
    pairs["".join(pair)] += 1


def step(pairs):
    new_pairs = defaultdict(int)
    for pair, counter in pairs.items():
        if pair in rules:
            replacements = rules[pair]
            new_pairs[replacements[0]] += counter
            new_pairs[replacements[1]] += counter
        else:
            new_pairs[pair] += counter
    return new_pairs

def run(pairs, steps):
    for _ in range(steps):
        pairs = step(pairs)

    counter = defaultdict(int)
    counter[letters[0]] += 1
    for pair, count in pairs.items():
        counter[pair[1]] += count

    return max(counter.values()) - min(counter.values())

print("Part 1: ", run(pairs.copy(), 10))
print("Part 2: ", run(pairs.copy(), 40))
