import sys


def is_horizontal(line):
    start, end = line
    return start[1] == end[1]


def is_vertical(line):
    start, end = line
    return start[0] == end[0]


def count_overlap(field):
    count = 0
    for row in field:
        for c in row:
            if c > 1:
                count += 1
    return count


def main():

    lines = []
    for line in open("input.txt"):
        items = line.rstrip("\n").split()
        start = tuple(int(item) for item in items[0].split(","))
        end = tuple(int(item) for item in items[2].split(","))
        lines.append((start, end))

    max_x = max(end[0] for start, end in lines)
    max_y = max(end[1] for start, end in lines)

    field = [[0 for x in range(max_x + 1)] for y in range(max_y + 1)]

    for line in lines:
        start, end = line
        if is_horizontal(line):
            y = start[1]
            x1, x2 = start[0], end[0]
            for x in range(min(x1, x2), max(x1, x2) + 1):
                field[y][x] += 1
        elif is_vertical(line):
            x = start[0]
            y1, y2 = start[1], end[1]
            for y in range(min(y1, y2), max(y1, y2) + 1):
                field[y][x] += 1
        else:  # diagonal
            x_dir = 1 if end[0] > start[0] else -1
            y_dir = 1 if end[1] > start[1] else -1
            length = abs(end[0] - start[0])
            for i in range(length + 1):
                field[start[1] + i * y_dir][start[0] + i * x_dir] += 1

    overlap = count_overlap(field)
    print(overlap)


if __name__ == "__main__":
    main()
