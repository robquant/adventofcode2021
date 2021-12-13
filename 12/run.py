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

path_count = 0


def find_paths(path, allowed):
    global path_count
    tail = path[-1]
    for neighbour in neighbours[tail]:
        if neighbour == "end":
            path_count += 1
            continue
        if allowed(path, neighbour):
            path.append(neighbour)
            find_paths(path, allowed)
            path.pop()


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
            # At this point we know that new_element is also in path
            # As el appears twice in the path, we can't add new_element
            return False
        counter.add(el)
    return True


find_paths(["start"], small_only_once)
print("Part 1: ", path_count)
path_count = 0
start = time.time()
find_paths(["start"], single_small_twice)
print("Part 2", path_count)
print(f"Runtime: {time.time() - start} sec")
