import math

target_x = (150, 193)
target_y = (-136, -86)

# target_x = (20, 30)
# target_y = (-10, -5)


def simulate(v_x, v_y):
    x, y = 0, 0
    max_y = -99999
    hits = False

    while True:
        x += v_x
        y += v_y
        if v_x > 0:
            v_x -= 1
        elif v_x < 0:
            v_x += 1
        v_y -= 1
        max_y = max(y, max_y)
        if target_x[0] <= x <= target_x[1] and target_y[0] <= y <= target_y[1]:
            hits = True
            break
        if x > target_x[1]:
            break
        if y < target_y[0]:
            break

    return hits, max_y


min_x = math.floor((2 * target_x[0]) ** 0.5) - 1
max_y = -9999
in_target = 0
for v_x in range(min_x, target_x[1] + 1):
    for v_y in range(target_y[0] - 1, 200):
        hits, max_y_ = simulate(v_x, v_y)
        if hits:
            max_y = max(max_y, max_y_)
            in_target += 1

print("Part 1:", max_y)
print("Part 2:", in_target)
