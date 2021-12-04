import sys
from collections import defaultdict


class Board:
    def __init__(self, grid_lines):
        self.board = [[False] * 5 for _ in range(5)]
        self.lookup = defaultdict(list)
        for i_row, line in enumerate(grid_lines):
            for i_col, number in enumerate(line):
                self.lookup[number].append((i_row, i_col))

    def scratch(self, number):
        if number in self.lookup:
            for field in self.lookup[number]:
                row, col = field
                self.board[row][col] = True

    def clear(self):
        self.board = [[False] * 5 for _ in range(5)]

    def has_won(self):
        for row in self.board:
            if all(row):
                return True
        for i_col in range(len(self.board[0])):
            if all(row[i_col] for row in self.board):
                return True
        return False

    def sum_unmarked(self):
        s = 0
        for number in self.lookup.keys():
            for field in self.lookup[number]:
                row, col = field
                if not self.board[row][col]:
                    s += number
        return s

    def __str__(self):
        res = []
        for row in self.board:
            line = []
            for field in row:
                if field:
                    line.append("X")
                else:
                    line.append("O")
            res.append(line)
        return "\n".join(" ".join(line) for line in res)


infile = "input.txt" if len(sys.argv) == 1 else sys.argv[1]
with open(infile) as inf:
    numbers = [int(number) for number in inf.readline().split(",")]

    lines = [line.rstrip("\n") for line in inf.readlines()]
    boards = []
    board_lines = []
    for line in lines:
        if line == "":
            if len(board_lines) > 0:
                boards.append(Board(board_lines))
                board_lines.clear()
                continue
            continue
        board_lines.append([int(number) for number in line.split()])
    if board_lines:
        boards.append(Board(board_lines))

win_scores = []
for number in numbers:
    for board in boards:
        board.scratch(number)
    won = [board for board in boards if board.has_won()]
    if won:
        win_scores.append(number * won[0].sum_unmarked())
    boards = [board for board in boards if not board.has_won()]
    if not boards:
        break

print("Part 1: ", win_scores[0])
print("Part 2: ", win_scores[-1])
