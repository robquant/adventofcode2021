import statistics
import math

crabs = [int(n) for n in open("input.txt").readline().split(",")]

# Part 1

align = statistics.median(crabs)
cost = sum(abs(crab - align) for crab in crabs)
print("Part 1: ", int(cost))

# Part 2
mean = statistics.mean(crabs)
candidates = [math.floor(mean), math.ceil(mean)]


def cost_func(crab, align):
    diff = abs(crab - align)
    return diff * (diff + 1) / 2


cost = sum(cost_func(crab, candidates[0]) for crab in crabs)
cost = min(cost, sum(cost_func(crab, candidates[1]) for crab in crabs))

print("Part 2: ", int(cost))
