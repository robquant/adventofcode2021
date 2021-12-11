import sys
import itertools


def flash(octo, neighbours):
    nflashes = 0
    nrows = len(octo)
    ncols = len(octo[1])
    for row in range(nrows):
        for col in range(ncols):
            if octo[row][col] > 9:
                nflashes += 1
                octo[row][col] = 0
                for neigh_row, neigh_col in neighbours[row, col]:
                    if octo[neigh_row][neigh_col] > 0:
                        octo[neigh_row][neigh_col] += 1
    return nflashes


def step(octo, neighbours):
    # Increase each octopus energy level by one
    nrows = len(octo)
    ncols = len(octo[1])
    for row in range(nrows):
        for col in range(ncols):
            octo[row][col] += 1
    total_flashes = 0
    while (nflashes := flash(octo, neighbours)) > 0:
        total_flashes += nflashes
    return total_flashes


def main():
    infile = "input.txt" if len(sys.argv) == 1 else sys.argv[1]

    octo = []
    for line in open(infile):
        line = line.rstrip("\n")
        octo.append([int(c) for c in line])

    orig = [row[:] for row in octo]

    neighbours = {}
    nrows = len(octo)
    ncols = len(octo[1])
    for row, col in itertools.product(range(nrows), range(ncols)):
        neighbours[(row, col)] = []
        for step_row, step_col in itertools.product((-1, 0, 1), (-1, 0, 1)):
            if step_row == 0 and step_col == 0:
                continue
            n_row = row + step_row
            n_col = col + +step_col
            if 0 <= n_row < nrows and 0 <= n_col < ncols:
                neighbours[(row, col)].append((n_row, n_col))

    nflashes = sum(step(octo, neighbours) for _ in range(100))
    print("Part 1: ", nflashes)

    octo = orig
    total_octopusses = nrows * ncols
    count = 1
    while step(octo, neighbours) < total_octopusses:
        count += 1
    print("Part 2: ", count)


if __name__ == "__main__":
    main()
