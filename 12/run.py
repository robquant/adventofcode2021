import sys
import time
from collections import defaultdict

infile = "input.txt" if len(sys.argv) == 1 else sys.argv[1]

neighbours = defaultdict(list)
for line in open(infile):
    a, b = line.rstrip("\n").split("-")
    if a != "end" and b != "start":
        neighbours[a].append(b)
    if a != "start" and b != "end":
        neighbours[b].append(a)

paths = []


def find_paths(path, allowed):
    tail = path[-1]
    for neighbour in neighbours[tail]:
        if neighbour == "end":
            paths.append(path + ["end"])
            continue
        if allowed(path, neighbour):
            find_paths(path + [neighbour], allowed)


def small_only_once(path, new_element):
    return not (new_element.islower() and new_element in path)


def single_small_twice(path, new_element):
    if not new_element.islower():
        return True
    if new_element not in path:
        return True
    counter = set()
    for el in path:
        if not el.islower():
            continue
        if el in counter:
            return False
        counter.add(el)
    return True


find_paths(["start"], small_only_once)
print("Part 1: ", len(paths))
paths.clear()
start = time.time()
find_paths(["start"], single_small_twice)
print("Part 2", len(paths))
print(f"Runtime: {time.time() - start} sec")
