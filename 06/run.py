import sys
import time

infile = "input.txt" if len(sys.argv) == 1 else sys.argv[1]
numbers = [int(item) for item in open(infile).readline().split(",")]
counts = [0] * 9
for number in numbers:
    counts[number] += 1


def simulate(jellyfish, days):
    counts = jellyfish[:]
    for _ in range(days):
        new_fish = counts[0]
        for i in range(1, 9):
            counts[i - 1] = counts[i]
        counts[6] += new_fish
        counts[8] = new_fish

    return sum(counts)


start = time.time()
print("Part 1", simulate(counts, 80))
print("Part 2", simulate(counts, 256))
print(f"{1000 * (time.time() - start)} ms")
