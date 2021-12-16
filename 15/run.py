import sys
import time
from dijkstra import calculate_distances


def find_neighbours(nrows, ncols, row, col):
    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        if 0 <= row + dy < nrows and 0 <= col + dx < ncols:
            yield (row + dy, col + dx)


def build_graph(array):
    nrows = len(array)
    ncols = len(array[0])
    graph = {}
    for y in range(nrows):
        for x in range(ncols):
            neighbours = {
                n: array[n[1]][n[0]] for n in find_neighbours(nrows, ncols, x, y)
            }
            graph[(x, y)] = neighbours
    return graph


infile = "input.txt" if len(sys.argv) == 1 else sys.argv[1]
array = [[int(c) for c in line.rstrip("\n")] for line in open(infile)]

nrows = len(array)
ncols = len(array[0])
graph = build_graph(array)
print("Part 1:", calculate_distances(graph, (0, 0))[nrows - 1, ncols - 1])

nrows_big = 5 * len(array)
ncols_big = 5 * len(array[0])
array_big = [[None] * ncols_big for _ in range(nrows_big)]
for repeat_x in range(5):
    for repeat_y in range(5):
        offset_x = repeat_x * ncols
        offset_y = repeat_y * nrows
        for row in range(nrows):
            for col in range(ncols):
                value = (array[row][col] + repeat_x + repeat_y) % 9
                if value == 0:
                    value = 9
                array_big[row + offset_x][col + offset_y] = value


graph = build_graph(array_big)
print("Part 2:", calculate_distances(graph, (0, 0))[nrows_big - 1, ncols_big - 1])
