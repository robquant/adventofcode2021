import sys
from collections import defaultdict

def count(bitstrings, pos, val):
    count = 0
    for bitstring in bitstrings:
        count += (bitstring[pos] == val)
    return count

def most_common(bitstrings, pos):
    ones = count(bitstrings, pos, "1")
    zeros = count(bitstrings, pos, "0")
    if ones >= zeros:
        return "1"
    return "0"

def least_common(bitstrings, pos):
    ones = count(bitstrings, pos, "1")
    zeros = count(bitstrings, pos, "0")
    if ones >= zeros:
        return "0"
    return "1"

input = "input.txt" if len(sys.argv) == 1 else sys.argv[1]
bitstrings = [line.rstrip("\n") for line in open(input)]

gamma = (most_common(bitstrings, pos) for pos in range(len(bitstrings[0])))
delta = (least_common(bitstrings, pos) for pos in range(len(bitstrings[0])))

print(int("".join(gamma), 2) * int("".join(delta), 2))

generator = bitstrings[:]
pos = 0
while len(generator) > 1:
    target = most_common(generator, pos)
    generator = [s for s in generator if s[pos] == target]
    pos += 1
assert len(generator) == 1

scrubber = bitstrings[:]
pos = 0
while len(scrubber) > 1:
    target = least_common(scrubber, pos)
    scrubber = [s for s in scrubber if s[pos] == target]
    pos += 1
assert len(scrubber) == 1

print(int(generator[0], 2) * int(scrubber[0], 2))