import sys
from collections import deque

infile = "input.txt" if len(sys.argv) == 1 else sys.argv[1]
grid = []

for line in open(infile):
    items = [int(item) for item in line.rstrip("\n")]
    grid.append(items)


def neighbours(rows, cols, pos):
    x, y = pos
    if x > 0:
        yield x - 1, y
    if y > 0:
        yield x, y - 1
    if x < cols - 1:
        yield x + 1, y
    if y < rows - 1:
        yield x, y + 1


rows = len(grid)
cols = len(grid[0])
low_points = []
for row in range(rows):
    for col in range(cols):
        number = grid[row][col]
        if all(number < grid[n[1]][n[0]] for n in neighbours(rows, cols, (col, row))):
            low_points.append((col, row))

s = sum(grid[p[1]][p[0]] + 1 for p in low_points)

print("Part 1: ", s)


def basin_from_point(grid, visited, start):
    rows = len(grid)
    cols = len(grid[0])
    basin = []
    stack = deque([start])
    while stack:
        point = stack.pop()
        if point in visited:
            continue
        point_val = grid[point[1]][point[0]]
        visited.add(point)
        basin.append(point)
        for n in neighbours(rows, cols, point):
            val = grid[n[1]][n[0]]
            if val != 9 and val not in visited and val > point_val:
                stack.append(n)
    return basin


visited = set()
basins = [len(basin_from_point(grid, visited, point)) for point in low_points]
basins.sort(reverse=True)
print("Part 2: ", basins[0] * basins[1] * basins[2])
