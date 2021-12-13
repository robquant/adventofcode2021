import sys
import operator


def to_str(paper):
    return "\n".join("".join(row) for row in paper)


infile = "input.txt" if len(sys.argv) == 1 else sys.argv[1]
DOT = "#"
EMPTY = "."


def read(infile):
    coords = []
    folds = []
    for line in open(infile):
        if "," in line:
            items = line.rstrip("\n").split(",")
            coords.append((int(items[0]), int(items[1])))
        elif "=" in line:
            line = line.rstrip("\n")
            xy, number = line.split(" ")[-1].split("=")
            folds.append((xy, int(number)))

    nrows = max(c[1] for c in coords) + 1
    ncols = max(c[0] for c in coords) + 1

    paper = [[EMPTY] * ncols for _ in range(nrows)]
    for coord in coords:
        col, row = coord
        paper[row][col] = DOT
    return paper, folds


def merge_rows(paper, i_src, i_target):
    src = paper[i_src]
    target = paper[i_target]
    for i, c in enumerate(src):
        if c == DOT:
            target[i] = DOT


def merge_columns(paper, i_src, i_target):
    ncols = len(paper)
    for i in range(ncols):
        if paper[i][i_src] == DOT:
            paper[i][i_target] = DOT


def fold_up(paper, y):
    nrows_to_fold = len(paper) - y
    for i in range(nrows_to_fold):
        merge_rows(paper, y + i, y - i)
    return paper[:y]


def fold_left(paper, x):
    ncols_to_fold = len(paper[0]) - x
    for i in range(ncols_to_fold):
        merge_columns(paper, x + i, x - i)
    return [row[:x] for row in paper]


paper, folds = read(infile)
for fold in folds:
    x_y, row_col = fold
    if x_y == "x":
        paper = fold_left(paper, row_col)
    elif x_y == "y":
        paper = fold_up(paper, row_col)
    else:
        raise ValueError(str(fold))
    print(sum(row.count(DOT) for row in paper))
print(to_str(paper))
