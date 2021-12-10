opening = list("({[<")
closing = list(")}]>")

matching = dict(zip(opening, closing))
error_scores = {")": 3, "]": 57, "}": 1197, ">": 25137}
completion_scores = {")": 1, "]": 2, "}": 3, ">": 4}


def is_opening(c):
    return c in opening


def is_closing(c):
    return c in closing


def is_matching(o, c):
    return matching[o] == c


def is_corrupted(line):
    stack = []
    for index, c in enumerate(line):
        if is_opening(c):
            stack.append(c)
        elif is_closing(c):
            o = stack.pop()
            if not is_matching(o, c):
                return True, (index, c, matching[o])
        else:
            raise ValueError("Unknown")
    return False, stack


def completion_score(open_parentheses):
    score = 0
    while open_parentheses:
        score *= 5
        c = open_parentheses.pop()
        score += completion_scores[matching[c]]
    return score


error_score = 0
completion_scores_lines = []
for line in open("input.txt"):
    line = line.rstrip("\n")
    error, result = is_corrupted(line)
    if error:
        index, found, expected = result
        error_score += error_scores[found]
    else:
        completion_scores_lines.append(completion_score(result))

completion_scores_lines.sort()
print("Part 1: ", error_score)
print("Part 2: ", completion_scores_lines[len(completion_scores_lines) // 2])
